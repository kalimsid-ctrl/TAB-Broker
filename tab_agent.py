import os
import requests
import google.generativeai as genai
import sys

# 1. Check if the API Key exists
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY is missing! Check your GitHub Secrets.")
    sys.exit(1)

# 2. Setup AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_market_data():
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
        response = requests.get(url, timeout=10)
        return response.json().get('pairs', [])[:5]
    except Exception as e:
        print(f"❌ API Error: {e}")
        return []

# Main Execution
pairs = get_market_data()
if not pairs:
    print("⚠️ No market data found.")
else:
    for coin in pairs:
        try:
            prompt = f"Analyze {coin['baseToken']['name']} as a crypto broker. Is it a good buy? Reply in 1 sentence."
            response = model.generate_content(prompt)
            print(f"✅ {coin['baseToken']['symbol']}: {response.text}")
        except Exception as e:
            print(f"❌ AI Analysis failed for {coin['baseToken']['symbol']}: {e}")
