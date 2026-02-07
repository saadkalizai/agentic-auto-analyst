import json
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_llm import BaseLLM

class TaskPlanner:
    """Agent that breaks down complex problems into actionable subtasks"""
    
    def __init__(self, model: str = None, temperature: float = 0.3):
        """
        Initialize the Task Planner
        
        Args:
            model: LLM model to use
            temperature: Lower temperature for more structured planning
        """
        self.llm = BaseLLM(model=model, temperature=temperature)
        
        # Planning prompt template
        self.planning_prompt = """You are an expert task planner. Your job is to break down complex problems into clear, actionable subtasks.

USER PROBLEM: {problem}

INSTRUCTIONS:
1. Analyze the problem and identify the key components
2. Break it down into 3-6 logical subtasks
3. Each subtask should be specific and actionable
4. Consider research, analysis, validation, and reporting phases
5. Output in JSON format with this structure:
{{
    "problem": "Original problem",
    "subtasks": [
        {{
            "id": 1,
            "task": "Specific task description",
            "agent": "Which agent should handle this (researcher, analyst, critic, etc.)",
            "tools": ["tools needed"],
            "expected_output": "What this task should produce"
        }}
    ],
    "rationale": "Brief explanation of why you chose this breakdown"
}}

OUTPUT ONLY VALID JSON:"""
    
    def create_plan(self, problem: str) -> Dict[str, Any]:
        """
        Create a task breakdown plan for a given problem
        
        Args:
            problem: The user's problem/query
            
        Returns:
            Dictionary containing the task breakdown
        """
        prompt = self.planning_prompt.format(problem=problem)
        
        try:
            # Get response from LLM
            response = self.llm(prompt)
            
            # Extract JSON from response
            json_str = self._extract_json(response)
            
            # Parse JSON
            plan = json.loads(json_str)
            
            # Validate structure
            self._validate_plan(plan)
            
            return plan
            
        except Exception as e:
            print(f"Error creating plan: {e}")
            # Return a simple default plan if parsing fails
            return self._create_default_plan(problem)
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from LLM response"""
        # Find JSON start and end
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start >= 0 and end > start:
            return text[start:end]
        else:
            # If no JSON found, wrap the text in a basic structure
            return json.dumps({
                "problem": "Parsing failed",
                "subtasks": [{
                    "id": 1,
                    "task": "Handle parsing error",
                    "agent": "system",
                    "tools": [],
                    "expected_output": "Error message"
                }],
                "rationale": "JSON parsing failed from LLM response"
            })
    
    def _validate_plan(self, plan: Dict[str, Any]):
        """Validate the plan structure"""
        required_keys = ["problem", "subtasks", "rationale"]
        for key in required_keys:
            if key not in plan:
                raise ValueError(f"Missing required key in plan: {key}")
        
        if not isinstance(plan["subtasks"], list):
            raise ValueError("Subtasks must be a list")
    
    def _create_default_plan(self, problem: str) -> Dict[str, Any]:
        """Create a default plan if LLM fails"""
        return {
            "problem": problem,
            "subtasks": [
                {
                    "id": 1,
                    "task": "Research and gather information about the problem",
                    "agent": "researcher",
                    "tools": ["web_search"],
                    "expected_output": "Collection of relevant information and sources"
                },
                {
                    "id": 2,
                    "task": "Analyze the gathered information",
                    "agent": "analyst",
                    "tools": [],
                    "expected_output": "Analysis of pros, cons, and insights"
                },
                {
                    "id": 3,
                    "task": "Validate the analysis and provide recommendations",
                    "agent": "critic",
                    "tools": [],
                    "expected_output": "Validated insights and actionable recommendations"
                }
            ],
            "rationale": "Default three-step research pipeline"
        }
    
    def display_plan(self, plan: Dict[str, Any]):
        """Display the plan in a readable format"""
        print("\n" + "="*60)
        print("📋 TASK PLAN")
        print("="*60)
        print(f"Problem: {plan['problem']}")
        print(f"\nRationale: {plan['rationale']}")
        print("\nSubtasks:")
        print("-"*60)
        
        for task in plan["subtasks"]:
            print(f"\n{task['id']}. {task['task']}")
            print(f"   🤖 Agent: {task['agent']}")
            print(f"   🛠️  Tools: {', '.join(task['tools']) if task['tools'] else 'None'}")
            print(f"   📄 Output: {task['expected_output']}")


# Test the Task Planner
if __name__ == "__main__":
    planner = TaskPlanner()
    
    # Test with a sample problem
    test_problem = "Analyze whether AI interview prep tools are a good startup idea in South Asia."
    
    print("Testing Task Planner...")
    print(f"Problem: {test_problem}")
    
    plan = planner.create_plan(test_problem)
    planner.display_plan(plan)
    
    # Save plan to file
    with open("examples/test_plan.json", "w") as f:
        json.dump(plan, f, indent=2)
    print("\n✅ Plan saved to 'examples/test_plan.json'") 
