import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("SERP_API_KEY")

if not api_key:
    print("❌ No API key")
    exit()

try:
    from serpapi import GoogleSearch
    
    params = {
        "q": "data science masters career",
        "api_key": api_key,
        "num": 3
    }
    
    print("🔍 Testing SERP API search...")
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "organic_results" in results:
        print(f"✅ Success! Found {len(results['organic_results'])} results")
        for r in results["organic_results"][:2]:
            print(f"\n📰 {r.get('title', 'No title')[:60]}...")
    else:
        print("❌ No results found")
        
except Exception as e:
    print(f"❌ Error: {e}") 
