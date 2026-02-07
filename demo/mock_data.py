"""
Mock data system for demo mode
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any

class MockDataGenerator:
    """Generate realistic mock data for demonstration"""
    
    @staticmethod
    def generate_mock_plan(problem: str) -> Dict[str, Any]:
        """Generate a mock task plan"""
        plans = {
            "startup_idea": {
                "problem": problem,
                "rationale": "This breakdown covers market validation, competitive analysis, technical feasibility, and financial modeling to thoroughly evaluate the startup potential.",
                "subtasks": [
                    {
                        "id": 1,
                        "task": "Research market size and growth trends",
                        "agent": "researcher",
                        "tools": ["market_reports", "industry_data"],
                        "expected_output": "Market size estimate and growth projections"
                    },
                    {
                        "id": 2,
                        "task": "Analyze competitor landscape and differentiation",
                        "agent": "analyst",
                        "tools": ["competitor_analysis"],
                        "expected_output": "Competitive analysis matrix and SWOT"
                    },
                    {
                        "id": 3,
                        "task": "Evaluate technical requirements and feasibility",
                        "agent": "technical_expert",
                        "tools": ["tech_assessment"],
                        "expected_output": "Technical feasibility report"
                    }
                ]
            },
            "market_analysis": {
                "problem": problem,
                "rationale": "Comprehensive market analysis covering demand drivers, segmentation, and regional variations.",
                "subtasks": [
                    {
                        "id": 1,
                        "task": "Analyze demand drivers and customer segments",
                        "agent": "researcher",
                        "tools": ["customer_surveys", "market_data"],
                        "expected_output": "Customer segmentation analysis"
                    },
                    {
                        "id": 2,
                        "task": "Research regional market variations",
                        "agent": "researcher",
                        "tools": ["regional_data", "demographics"],
                        "expected_output": "Regional breakdown report"
                    }
                ]
            }
        }
        
        # Select appropriate plan based on problem keywords
        problem_lower = problem.lower()
        if any(word in problem_lower for word in ["startup", "business idea", "venture"]):
            return plans["startup_idea"]
        else:
            return plans["market_analysis"]
    
    @staticmethod
    def generate_mock_research(task_description: str) -> Dict[str, Any]:
        """Generate mock research results"""
        
        # Sample data templates
        tech_templates = [
            {
                "title": "AI Adoption Growing at 40% CAGR in Target Region",
                "snippet": "Recent industry reports indicate rapid adoption of AI solutions, with the interview preparation segment showing particularly strong growth.",
                "url": "https://techreport.example/ai-growth-2024",
                "credibility": "high"
            },
            {
                "title": "Market Size Estimated at $850M with Strong Growth Projections",
                "snippet": "The target market is projected to reach $1.2B by 2026, driven by increasing digital literacy and job market competition.",
                "url": "https://marketresearch.example/size-projections",
                "credibility": "medium"
            }
        ]
        
        startup_templates = [
            {
                "title": "Success Stories: Similar Startups Securing Series A Funding",
                "snippet": "Three startups in adjacent spaces have raised over $20M in combined funding in the last 12 months.",
                "url": "https://startuptracker.example/funding-stories",
                "credibility": "high"
            },
            {
                "title": "Customer Willingness to Pay: Survey Results",
                "snippet": "68% of surveyed professionals indicated willingness to pay $20-50/month for premium interview preparation tools.",
                "url": "https://surveydata.example/willingness-pay",
                "credibility": "medium"
            }
        ]
        
        # Select appropriate templates
        templates = tech_templates if any(word in task_description.lower() for word in ["tech", "ai", "software"]) else startup_templates
        
        return {
            "topic": task_description,
            "summary": f"Research indicates strong potential for {task_description.split()[0]} with several key opportunities identified.",
            "key_findings": [
                {
                    "category": "Market Opportunity",
                    "points": [
                        "Growing demand in target demographic (18-35 age group)",
                        "Increasing digital adoption post-pandemic",
                        "Limited existing high-quality solutions"
                    ]
                },
                {
                    "category": "Competitive Landscape",
                    "points": [
                        "2-3 major players with 60% market share",
                        "Several smaller niche competitors",
                        "Opportunity for differentiation through AI personalization"
                    ]
                }
            ],
            "statistics": [
                "Market growth: 25% YoY",
                "Target audience size: 15M potential users",
                "Average revenue per user: $180 annually"
            ],
            "sources": random.sample(templates, min(2, len(templates))),
            "gaps": [
                "Region-specific cultural adaptation data",
                "Long-term user retention metrics"
            ],
            "next_steps": [
                "Conduct user interviews for validation",
                "Analyze regional regulatory requirements"
            ]
        }
    
    @staticmethod
    def generate_mock_critique(research: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock critique"""
        
        # Determine quality score based on content
        has_stats = len(research.get("statistics", [])) > 0
        has_sources = len(research.get("sources", [])) > 0
        
        completeness = 7 if has_stats and has_sources else 5
        accuracy = 8 if has_sources else 6
        
        return {
            "topic": research.get("topic", "Unknown"),
            "validation": {
                "completeness_score": completeness,
                "accuracy_score": accuracy,
                "source_credibility_score": 7,
                "biases_identified": ["Optimism bias in growth projections"],
                "assumptions": ["Current trends will continue", "No major regulatory changes"]
            },
            "critique": {
                "strengths": [
                    "Comprehensive market data",
                    "Clear opportunity identification",
                    "Actionable insights provided"
                ],
                "weaknesses": [
                    "Limited primary research",
                    "Regional variations not fully addressed"
                ],
                "logical_issues": ["Correlation vs causation in trend analysis"],
                "missing_perspectives": ["User experience considerations", "Implementation challenges"]
            },
            "improvements": [
                {
                    "area": "Primary Research",
                    "suggestion": "Conduct 20-30 user interviews for validation",
                    "priority": "high"
                },
                {
                    "area": "Regional Analysis",
                    "suggestion": "Break down analysis by country/region",
                    "priority": "medium"
                }
            ],
            "overall_quality": (completeness + accuracy) // 2,
            "confidence_level": "medium",
            "recommendation": "Proceed with cautious optimism. Validate key assumptions with primary research."
        }
    
    @staticmethod
    def generate_mock_report(problem: str, plan: Dict, research_items: List, critiques: List) -> Dict[str, Any]:
        """Generate complete mock report"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "metadata": {
                "problem": problem,
                "generated_at": timestamp,
                "total_tasks": len(plan.get("subtasks", [])),
                "research_tasks_completed": len(research_items),
                "mode": "demo"
            },
            "executive_summary": {
                "problem_statement": problem,
                "key_insights": [
                    "Strong market growth identified (25% YoY)",
                    "Clear differentiation opportunities available",
                    "Moderate competitive intensity"
                ],
                "overall_quality_score": 7,
                "confidence_level": "medium",
                "top_recommendation": "Develop MVP and conduct pilot testing with target users"
            },
            "recommendations": [
                "Proceed with MVP development focusing on core AI features",
                "Secure pilot customers for validation",
                "Develop detailed go-to-market strategy",
                "Assemble advisory board with regional expertise"
            ],
            "next_steps": [
                "Week 1-2: Finalize feature set and technical specifications",
                "Week 3-4: Develop MVP prototype",
                "Week 5-6: Conduct pilot testing with 20 users",
                "Week 7-8: Iterate based on feedback"
            ]
        }
    
    @staticmethod
    def get_sample_problems() -> List[Dict[str, str]]:
        """Get sample problems for the gallery"""
        return [
            {
                "id": "startup_ai_interview",
                "title": "AI Interview Prep Startup",
                "description": "Analyze whether AI interview prep tools are a good startup idea in South Asia",
                "category": "startup",
                "difficulty": "medium"
            },
            {
                "id": "market_ev_asia",
                "title": "EV Market in Southeast Asia",
                "description": "Analyze the electric vehicle market growth potential in Southeast Asia",
                "category": "market",
                "difficulty": "hard"
            },
            {
                "id": "tech_ai_healthcare",
                "title": "AI in Healthcare Diagnosis",
                "description": "Evaluate the adoption of AI in healthcare diagnosis in developing countries",
                "category": "tech",
                "difficulty": "hard"
            },
            {
                "id": "business_food_delivery",
                "title": "Food Delivery in Rural Areas",
                "description": "Analyze the potential for a food delivery app in rural areas with limited infrastructure",
                "category": "business",
                "difficulty": "medium"
            }
        ]


# Quick test
if __name__ == "__main__":
    generator = MockDataGenerator()
    
    print("🧪 Testing Mock Data Generator")
    print("=" * 40)
    
    # Test plan generation
    problem = "Test startup idea"
    plan = generator.generate_mock_plan(problem)
    print(f"✅ Plan generated: {len(plan['subtasks'])} tasks")
    
    # Test research generation
    research = generator.generate_mock_research("Market research")
    print(f"✅ Research generated: {len(research['key_findings'])} findings")
    
    # Test critique generation
    critique = generator.generate_mock_critique(research)
    print(f"✅ Critique generated: Score {critique['overall_quality']}/10")
    
    # Test sample problems
    samples = generator.get_sample_problems()
    print(f"✅ {len(samples)} sample problems available")
    
    print("\n🎯 Mock data system ready for UI development!")