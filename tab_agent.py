import os
import requests
import google.generativeai as genai

# 1. Setup AI (Gemini)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_market_data():
    # Fetching trending coins from DexScreener (Free API)
    # Focuses on Solana as per your previous project interest
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    response = requests.get(url).json()
    return response['pairs'][:5]  # Get top 5 pairs

def analyze_with_tab(coin):
    prompt = f"""
    Analyze this crypto coin for a 'Trusted Broker' score (0-100).
    Name: {coin['baseToken']['name']}
    Volume (24h): {coin['volume']['h24']}
    Liquidity: {coin['liquidity']['usd']}
    
    If the liquidity is low or volume looks fake, give a low score.
    Return only a JSON: {{"score": 85, "reason": "High organic volume"}}
    """
    response = model.generate_content(prompt)
    return response.text

# Main Execution
pairs = get_market_data()
for coin in pairs:
    analysis = analyze_with_tab(coin)
    print(f"TAB Analysis for {coin['baseToken']['symbol']}: {analysis}")
