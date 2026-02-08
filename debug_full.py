import json
from agents.researcher import ResearchAgent

researcher = ResearchAgent()
query = "study in germany vs other european countries"

print("🔍 FULL DEBUG")
print("="*60)

# Test search directly
print("1. Testing search_web()...")
results = researcher.search_web(query, max_results=2)
print(f"   Raw results: {len(results)}")

if results:
    print(f"\n2. Sample result:")
    print(f"   Title: {results[0]['title']}")
    print(f"   URL: {results[0]['url']}")
    
    # Test research_topic
    print(f"\n3. Testing research_topic()...")
    research = researcher.research_topic(query)
    
    print(f"\n4. Research output:")
    print(f"   Summary: {research.get('summary', 'NO SUMMARY')}")
    print(f"   Has findings: {len(research.get('key_findings', []))}")
    
    if research.get('key_findings'):
        print(f"\n5. First finding:")
        print(f"   {research['key_findings'][0]}")
else:
    print("\n❌ NO SEARCH RESULTS - Check SERP API key")
    
    # Check API key
    import os
    from dotenv import load_dotenv
    load_dotenv()
    print(f"\n🔑 SERP API Key exists: {bool(os.getenv('SERP_API_KEY'))}")
    print(f"   First 10 chars: {os.getenv('SERP_API_KEY', '')[:10]}...")