"""
Mock agents for demo mode
"""

import time
from typing import Dict, List, Any
from mock_data import MockDataGenerator
class MockTaskPlanner:
    """Mock task planner for demo mode"""
    
    def __init__(self):
        self.generator = MockDataGenerator()
    
    def create_plan(self, problem: str) -> Dict[str, Any]:
        """Create mock plan with simulated delay"""
        time.sleep(1)  # Simulate processing time
        return self.generator.generate_mock_plan(problem)
    
    def display_plan(self, plan: Dict[str, Any]):
        """Display plan (mock version)"""
        print(f"\n📋 Plan: {plan['problem'][:50]}...")
        print(f"   Tasks: {len(plan['subtasks'])}")

class MockResearchAgent:
    """Mock research agent for demo mode"""
    
    def __init__(self):
        self.generator = MockDataGenerator()
    
    def research_topic(self, topic: str, search_query: str = None) -> Dict[str, Any]:
        """Generate mock research with simulated delay"""
        time.sleep(2)  # Simulate search time
        return self.generator.generate_mock_research(topic)
    
    def display_research(self, research: Dict[str, Any]):
        """Display research (mock version)"""
        print(f"\n🔍 Research: {research['topic'][:50]}...")
        print(f"   Sources: {len(research.get('sources', []))}")

class MockCriticAgent:
    """Mock critic agent for demo mode"""
    
    def __init__(self):
        self.generator = MockDataGenerator()
    
    def critique_research(self, research: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock critique with simulated delay"""
        time.sleep(1)  # Simulate analysis time
        return self.generator.generate_mock_critique(research)
    
    def display_critique(self, critique: Dict[str, Any]):
        """Display critique (mock version)"""
        print(f"\n🎯 Critique: Score {critique['overall_quality']}/10")

class MockAutoAnalyst:
    """Complete mock analyst for demo mode"""
    
    def __init__(self, speed: str = "normal"):
        """
        Initialize mock analyst
        
        Args:
            speed: 'fast' (3s), 'normal' (6s), or 'realistic' (12s)
        """
        self.speeds = {
            "fast": 0.5,
            "normal": 1.0,
            "realistic": 2.0
        }
        self.speed_factor = self.speeds.get(speed, 1.0)
        
        self.planner = MockTaskPlanner()
        self.researcher = MockResearchAgent()
        self.critic = MockCriticAgent()
        self.generator = MockDataGenerator()
    
    def analyze(self, problem: str) -> Dict[str, Any]:
        """
        Run complete mock analysis pipeline
        
        Args:
            problem: User's problem
            
        Returns:
            Complete mock report
        """
        print(f"🚀 Starting mock analysis: {problem[:50]}...")
        
        # Step 1: Planning
        time.sleep(1 * self.speed_factor)
        plan = self.planner.create_plan(problem)
        
        # Step 2: Research
        research_items = []
        for task in plan["subtasks"]:
            time.sleep(2 * self.speed_factor)
            research = self.researcher.research_topic(task["task"])
            research_items.append({
                "task_id": task["id"],
                "task_description": task["task"],
                "research": research
            })
        
        # Step 3: Critique
        critiques = []
        for item in research_items:
            time.sleep(1 * self.speed_factor)
            critique = self.critic.critique_research(item["research"])
            critiques.append({
                "task_id": item["task_id"],
                "critique": critique
            })
        
        # Step 4: Final report
        time.sleep(1 * self.speed_factor)
        final_report = self.generator.generate_mock_report(
            problem, plan, research_items, critiques
        )
        
        return {
            "plan": plan,
            "research_items": research_items,
            "critiques": critiques,
            "final_report": final_report,
            "metadata": {
                "mode": "demo",
                "speed": self.speed_factor,
                "total_time": f"{4 + len(plan['subtasks']) * 3 * self.speed_factor:.1f}s"
            }
        }


# Quick test
if __name__ == "__main__":
    print("🧪 Testing Mock Agents")
    print("=" * 40)
    
    # Test fast mode
    analyst = MockAutoAnalyst(speed="fast")
    
    start_time = time.time()
    result = analyst.analyze(
        "Analyze whether AI interview prep tools are a good startup idea in South Asia."
    )
    elapsed = time.time() - start_time
    
    print(f"\n✅ Mock analysis complete in {elapsed:.1f}s")
    print(f"   Tasks: {len(result['plan']['subtasks'])}")
    print(f"   Research items: {len(result['research_items'])}")
    print(f"   Overall quality: {result['final_report']['executive_summary']['overall_quality_score']}/10") 
