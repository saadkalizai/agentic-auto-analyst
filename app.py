import json
import os
from datetime import datetime
from typing import Dict, Any

from agents.planner import TaskPlanner
from agents.researcher import ResearchAgent
from agents.critic import CriticAgent

class AutoAnalyst:
    """Main orchestrator for the Auto-Analyst system"""
    
    def __init__(self):
        """Initialize all agents"""
        self.planner = TaskPlanner()
        self.researcher = ResearchAgent()
        self.critic = CriticAgent()
        
        # Create output directory
        os.makedirs("outputs", exist_ok=True)
    
    def analyze(self, problem: str) -> Dict[str, Any]:
        """
        Main analysis pipeline
        
        Args:
            problem: User's problem/query
            
        Returns:
            Complete analysis report
        """
        print("🤖 AUTO-ANALYST SYSTEM")
        print("=" * 60)
        print(f"Problem: {problem}")
        print("=" * 60)
        
        # Step 1: Create task plan
        print("\n📋 STEP 1: Task Planning")
        print("-" * 40)
        plan = self.planner.create_plan(problem)
        self.planner.display_plan(plan)
        
        # Step 2: Execute research tasks
        print("\n🔍 STEP 2: Research Execution")
        print("-" * 40)
        
        all_research = []
        for task in plan["subtasks"]:
            if task["agent"] in ["researcher", "analyst", "data_scientist"]:
                print(f"\n📊 Researching: {task['task']}")
                research = self.researcher.research_topic(task["task"])
                self.researcher.display_research(research)
                all_research.append({
                    "task_id": task["id"],
                    "task_description": task["task"],
                    "research": research
                })
        
        # Step 3: Critique the findings
        print("\n🎯 STEP 3: Critical Analysis")
        print("-" * 40)
        
        all_critiques = []
        for research_item in all_research:
            print(f"\n🔍 Critiquing research for Task {research_item['task_id']}")
            critique = self.critic.critique_research(research_item["research"])
            self.critic.display_critique(critique)
            all_critiques.append({
                "task_id": research_item["task_id"],
                "critique": critique
            })
        
        # Step 4: Generate final report
        print("\n📄 STEP 4: Final Report Generation")
        print("-" * 40)
        
        final_report = self._generate_final_report(
            problem=problem,
            plan=plan,
            research_items=all_research,
            critiques=all_critiques
        )
        
        # Save everything
        self._save_analysis(
            problem=problem,
            plan=plan,
            research_items=all_research,
            critiques=all_critiques,
            final_report=final_report
        )
        
        return final_report
    
    def _generate_final_report(self, problem: str, plan: Dict, 
                              research_items: list, critiques: list) -> Dict[str, Any]:
        """Generate the final comprehensive report"""
        
        # Use the critic to evaluate overall quality
        combined_research = {
            "topic": f"Comprehensive analysis: {problem}",
            "summary": f"Analysis combining {len(research_items)} research tasks",
            "key_findings": [],
            "sources": []
        }
        
        # Combine key findings from all research
        for item in research_items:
            if "research" in item and "key_findings" in item["research"]:
                combined_research["key_findings"].extend(item["research"]["key_findings"])
            if "research" in item and "sources" in item["research"]:
                combined_research["sources"].extend(item["research"]["sources"])
        
        # Get overall critique
        overall_critique = self.critic.critique_research(combined_research)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(plan, research_items, critiques)
        
        # Create final report
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        final_report = {
            "metadata": {
                "problem": problem,
                "generated_at": timestamp,
                "total_tasks": len(plan["subtasks"]),
                "research_tasks_completed": len(research_items),
                "critiques_generated": len(critiques)
            },
            "executive_summary": {
                "problem_statement": problem,
                "key_insights": self._extract_key_insights(research_items),
                "overall_quality_score": overall_critique.get("overall_quality", 5),
                "confidence_level": overall_critique.get("confidence_level", "medium"),
                "top_recommendation": recommendations[0] if recommendations else "No clear recommendation"
            },
            "methodology": {
                "planning_rationale": plan.get("rationale", ""),
                "agents_used": ["TaskPlanner", "ResearchAgent", "CriticAgent"],
                "tools_used": ["Groq LLM", "DuckDuckGo Search"]
            },
            "detailed_findings": [
                {
                    "task_id": item["task_id"],
                    "task": item["task_description"],
                    "research_summary": item["research"].get("summary", ""),
                    "key_points": item["research"].get("key_findings", [])[:2]  # Top 2 points
                }
                for item in research_items
            ],
            "critical_assessment": {
                "overall_score": overall_critique.get("overall_quality", 5),
                "strengths": overall_critique.get("critique", {}).get("strengths", []),
                "weaknesses": overall_critique.get("critique", {}).get("weaknesses", []),
                "improvement_suggestions": overall_critique.get("improvements", [])
            },
            "recommendations": recommendations,
            "next_steps": self._generate_next_steps(critiques)
        }
        
        return final_report
    
    def _extract_key_insights(self, research_items: list) -> list:
        """Extract key insights from all research"""
        insights = []
        for item in research_items:
            research = item.get("research", {})
            if "summary" in research:
                insights.append(f"Task {item['task_id']}: {research['summary'][:150]}...")
        return insights[:5]  # Limit to 5 insights
    
    def _generate_recommendations(self, plan: Dict, research_items: list, critiques: list) -> list:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Add recommendations based on plan
        for task in plan["subtasks"]:
            if "recommend" in task["task"].lower() or "suggest" in task["task"].lower():
                recommendations.append(f"Consider: {task['task']}")
        
        # Add recommendations from critiques
        for critique_item in critiques:
            critique = critique_item.get("critique", {})
            if "recommendation" in critique:
                recommendations.append(f"Task {critique_item['task_id']}: {critique['recommendation']}")
        
        # Default recommendations if none found
        if not recommendations:
            recommendations = [
                "Conduct more targeted market research",
                "Validate findings with industry experts",
                "Analyze competitor offerings in detail",
                "Assess technical feasibility and costs",
                "Develop a minimum viable product (MVP) strategy"
            ]
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _generate_next_steps(self, critiques: list) -> list:
        """Generate next steps based on critiques"""
        next_steps = []
        
        for critique_item in critiques:
            critique = critique_item.get("critique", {})
            improvements = critique.get("improvements", [])
            for imp in improvements[:2]:  # Get top 2 improvements per critique
                if imp.get("priority") == "high":
                    next_steps.append(f"High priority: {imp.get('suggestion', '')}")
        
        if not next_steps:
            next_steps = [
                "Expand search to academic databases",
                "Conduct expert interviews",
                "Analyze regional market data",
                "Validate with user surveys"
            ]
        
        return next_steps[:5]
    
    def _save_analysis(self, problem: str, plan: Dict, research_items: list, 
                      critiques: list, final_report: Dict):
        """Save all analysis components to files"""
        
        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_problem = problem[:50].replace(" ", "_").replace("?", "").replace(".", "")
        
        # Save individual components
        components = {
            "plan": plan,
            "research": research_items,
            "critiques": critiques,
            "final_report": final_report
        }
        
        for name, data in components.items():
            filename = f"outputs/{timestamp}_{safe_problem}_{name}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  ✅ Saved {name}: {filename}")
        
        # Also save a simple text summary
        text_filename = f"outputs/{timestamp}_{safe_problem}_summary.txt"
        with open(text_filename, "w", encoding="utf-8") as f:
            f.write(f"AUTO-ANALYST REPORT\n")
            f.write(f"="*50 + "\n")
            f.write(f"Problem: {problem}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\nEXECUTIVE SUMMARY:\n")
            f.write(f"-"*30 + "\n")
            f.write(f"{final_report['executive_summary']['problem_statement']}\n\n")
            f.write(f"Key Insights:\n")
            for insight in final_report['executive_summary']['key_insights']:
                f.write(f"• {insight}\n")
            f.write(f"\nOverall Quality: {final_report['executive_summary']['overall_quality_score']}/10\n")
            f.write(f"Confidence: {final_report['executive_summary']['confidence_level'].upper()}\n")
            f.write(f"\nTOP RECOMMENDATION:\n")
            f.write(f"{final_report['executive_summary']['top_recommendation']}\n")
            
            f.write(f"\nRECOMMENDATIONS:\n")
            f.write(f"-"*30 + "\n")
            for i, rec in enumerate(final_report['recommendations'], 1):
                f.write(f"{i}. {rec}\n")
            
            f.write(f"\nNEXT STEPS:\n")
            f.write(f"-"*30 + "\n")
            for i, step in enumerate(final_report['next_steps'], 1):
                f.write(f"{i}. {step}\n")
        
        print(f"  ✅ Saved text summary: {text_filename}")
    
    def display_final_report(self, report: Dict[str, Any]):
        """Display the final report in readable format"""
        print("\n" + "="*60)
        print("📄 FINAL ANALYSIS REPORT")
        print("="*60)
        
        meta = report.get("metadata", {})
        print(f"\n📌 METADATA:")
        print(f"   Problem: {meta.get('problem', 'Unknown')}")
        print(f"   Generated: {meta.get('generated_at', 'Unknown time')}")
        print(f"   Tasks: {meta.get('total_tasks', 0)} planned, {meta.get('research_tasks_completed', 0)} completed")
        
        exec_summary = report.get("executive_summary", {})
        print(f"\n🎯 EXECUTIVE SUMMARY:")
        print(f"   Overall Quality: {exec_summary.get('overall_quality_score', 'N/A')}/10")
        print(f"   Confidence: {exec_summary.get('confidence_level', 'unknown').upper()}")
        
        print(f"\n💡 KEY INSIGHTS:")
        for insight in exec_summary.get("key_insights", [])[:3]:
            print(f"   • {insight}")
        
        print(f"\n🚀 TOP RECOMMENDATION:")
        print(f"   {exec_summary.get('top_recommendation', 'No recommendation')}")
        
        print(f"\n📋 DETAILED RECOMMENDATIONS:")
        for i, rec in enumerate(report.get("recommendations", [])[:5], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n🔄 NEXT STEPS:")
        for i, step in enumerate(report.get("next_steps", [])[:3], 1):
            print(f"   {i}. {step}")
        
        print(f"\n📁 Output saved to 'outputs/' directory")
        print("="*60)


# Main execution
if __name__ == "__main__":
    # Create the Auto-Analyst
    analyst = AutoAnalyst()
    
    # Example problem (you can change this)
    example_problem = "Analyze whether AI interview prep tools are a good startup idea in South Asia."
    
    # Alternatively, uncomment to take user input:
    # example_problem = input("Enter your problem/query: ")
    
    print("🚀 Starting Auto-Analyst...")
    print("Note: This will take 1-2 minutes as it performs web searches.")
    print("-" * 60)
    
    # Run the analysis
    try:
        final_report = analyst.analyze(example_problem)
        analyst.display_final_report(final_report)
        
        print("\n✅ Analysis complete! Check the 'outputs/' folder for detailed results.")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Please check your internet connection and API key.") 
