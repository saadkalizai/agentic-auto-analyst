import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERP_API_KEY")

if api_key:
    print(f"✅ SERP API Key found: {api_key[:10]}...")
else:
    print("❌ SERP_API_KEY not found in .env file") 
