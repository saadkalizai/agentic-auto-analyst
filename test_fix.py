from agents.researcher import ResearchAgent

researcher = ResearchAgent()

test_queries = [
    "is it a good idea to pursue your degree from germany as compared to other european countries",
    "should i study data science or artificial intelligence",
    "analyze the electric vehicle market in europe",
    "is ai interview prep a good startup idea"
]

print("🧪 Testing Query Optimizer Fix")
print("="*60)

for query in test_queries:
    optimized = researcher._optimize_query(query)
    print(f"\nOriginal: {query}")
    print(f"Optimized: {optimized}")
    print("-"*40)