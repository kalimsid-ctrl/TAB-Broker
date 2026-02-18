import os
import requests
import google.generativeai as genai
import json
from datetime import datetime

# Setup
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_market_data():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    return requests.get(url).json().get('pairs', [])[:3]

def save_trade(coin_data):
    file_path = 'trades.json'
    # 1. Load existing trades or start new list
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            trades = json.load(f)
    else:
        trades = []

    # 2. Add the new trade
    new_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "symbol": coin_data['baseToken']['symbol'],
        "price": coin_data['priceUsd'],
        "vibe_score": coin_data['vibe_score']
    }
    trades.append(new_entry)

    # 3. Save back to file
    with open(file_path, 'w') as f:
        json.dump(trades, f, indent=4)

# Run Logic
pairs = get_market_data()
for coin in pairs:
    prompt = f"Analyze {coin['baseToken']['name']} (SOL). Give a Trust Score 1-100. Return ONLY the number."
    score = model.generate_content(prompt).text.strip()
    
    # Paper trade if score is high
    if int(score) > 75:
        coin['vibe_score'] = score
        save_trade(coin)
        print(f"🚀 Paper Traded {coin['baseToken']['symbol']} with Score: {score}")
