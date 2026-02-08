 
from agents.researcher import ResearchAgent
from agents.critic import CriticAgent

# Create sample research
researcher = ResearchAgent()
query = "study in germany vs other european countries"
research = researcher.research_topic(query)

print("🧪 Testing Critic Agent")
print("="*60)
print(f"Research summary: {research['summary'][:100]}...")

# Test critic
critic = CriticAgent()
critique = critic.critique_research(research)

print(f"\nCritique scores:")
print(f"  Overall quality: {critique.get('overall_quality', 'N/A')}/10")
print(f"  Confidence: {critique.get('confidence_level', 'N/A')}")

if critique.get('overall_quality', 0) < 5:
    print(f"\n⚠️ Low score reasons:")
    validation = critique.get('validation', {})
    print(f"  Completeness: {validation.get('completeness_score', 'N/A')}/10")
    print(f"  Accuracy: {validation.get('accuracy_score', 'N/A')}/10")