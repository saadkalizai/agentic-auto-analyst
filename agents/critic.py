import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_llm import BaseLLM
class CriticAgent:
    """Agent that validates, critiques, and improves research findings"""
    
    def __init__(self, model: str = None, temperature: float = 0.4):
        """
        Initialize the Critic Agent
        
        Args:
            model: LLM model to use
            temperature: Lower temperature for critical analysis
        """
        self.llm = BaseLLM(model=model, temperature=temperature)
        
        # Critique prompt template
        self.critique_prompt = """You are an expert critical analyst. Your job is to validate, critique, and improve research findings.

RESEARCH TOPIC: {topic}

RESEARCH FINDINGS:
{findings}

INSTRUCTIONS:
1. Validate the completeness and accuracy of the findings
2. Identify biases, assumptions, or logical fallacies
3. Assess source credibility and potential conflicts
4. Suggest improvements or additional research needed
5. Rate the overall quality (1-10 scale)
6. Output in JSON format:
{{
    "topic": "Research topic",
    "validation": {{
        "completeness_score": 1-10,
        "accuracy_score": 1-10,
        "source_credibility_score": 1-10,
        "biases_identified": ["bias 1", "bias 2", ...],
        "assumptions": ["assumption 1", "assumption 2", ...]
    }},
    "critique": {{
        "strengths": ["strength 1", "strength 2", ...],
        "weaknesses": ["weakness 1", "weakness 2", ...],
        "logical_issues": ["issue 1", "issue 2", ...],
        "missing_perspectives": ["perspective 1", "perspective 2", ...]
    }},
    "improvements": [
        {{
            "area": "Area needing improvement",
            "suggestion": "Specific suggestion",
            "priority": "high/medium/low"
        }}
    ],
    "overall_quality": 1-10,
    "confidence_level": "high/medium/low",
    "recommendation": "Overall recommendation for use"
}}

OUTPUT ONLY VALID JSON:"""
    
    def critique_research(self, research: Dict[str, Any]) -> Dict[str, Any]:
        """
        Critique and validate research findings
        
        Args:
            research: Research results from ResearchAgent
            
        Returns:
            Critique analysis
        """
        # Prepare findings summary
        findings_summary = self._prepare_findings_summary(research)
        
        # Create prompt
        prompt = self.critique_prompt.format(
            topic=research.get("topic", "Unknown topic"),
            findings=findings_summary
        )
        
        try:
            # Get critique from LLM
            response = self.llm(prompt)
            
            # Extract JSON
            json_str = self._extract_json(response)
            
            # Parse JSON
            critique = json.loads(json_str)
            
            # Add metadata
            critique["research_topic"] = research.get("topic", "")
            critique["original_research_summary"] = research.get("summary", "")
            
            return critique
            
        except Exception as e:
            print(f"Critique error: {e}")
            return self._create_default_critique(research)
    
    def _prepare_findings_summary(self, research: Dict[str, Any]) -> str:
        """Prepare a summary of research findings for the critique"""
        summary_parts = []
        
        summary_parts.append(f"SUMMARY: {research.get('summary', 'No summary')}")
        
        if research.get('key_findings'):
            summary_parts.append("\nKEY FINDINGS:")
            for finding in research['key_findings']:
                summary_parts.append(f"- {finding['category']}:")
                for point in finding.get('points', [])[:3]:  # Limit to 3 points per category
                    summary_parts.append(f"  • {point}")
        
        if research.get('statistics'):
            summary_parts.append("\nSTATISTICS:")
            for stat in research['statistics'][:5]:  # Limit to 5 stats
                summary_parts.append(f"- {stat}")
        
        if research.get('sources'):
            summary_parts.append("\nSOURCES:")
            for source in research['sources'][:3]:  # Limit to 3 sources
                summary_parts.append(f"- {source.get('title', 'No title')} ({source.get('credibility', 'unknown')})")
        
        if research.get('gaps'):
            summary_parts.append("\nIDENTIFIED GAPS:")
            for gap in research['gaps'][:3]:  # Limit to 3 gaps
                summary_parts.append(f"- {gap}")
        
        return "\n".join(summary_parts)
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from LLM response"""
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start >= 0 and end > start:
            return text[start:end]
        else:
            # Fallback structure
            return json.dumps({
                "topic": "JSON extraction failed",
                "validation": {
                    "completeness_score": 5,
                    "accuracy_score": 5,
                    "source_credibility_score": 5,
                    "biases_identified": ["Could not parse critique"],
                    "assumptions": ["Parsing failed"]
                },
                "critique": {
                    "strengths": ["Critique system operational"],
                    "weaknesses": ["Could not generate proper critique"],
                    "logical_issues": ["Parsing error"],
                    "missing_perspectives": ["Full critique unavailable"]
                },
                "improvements": [{
                    "area": "Critique system",
                    "suggestion": "Retry critique generation",
                    "priority": "high"
                }],
                "overall_quality": 5,
                "confidence_level": "low",
                "recommendation": "Manual review required"
            })
    
    def _create_default_critique(self, research: Dict[str, Any]) -> Dict[str, Any]:
        """Create default critique if LLM fails"""
        return {
            "topic": research.get("topic", "Unknown"),
            "research_topic": research.get("topic", ""),
            "original_research_summary": research.get("summary", ""),
            "validation": {
                "completeness_score": 5,
                "accuracy_score": 5,
                "source_credibility_score": 5,
                "biases_identified": ["Unknown due to critique failure"],
                "assumptions": ["Default critique generated"]
            },
            "critique": {
                "strengths": ["Research was conducted", "Findings were documented"],
                "weaknesses": ["Critique system failed", "Limited validation"],
                "logical_issues": ["Unable to assess"],
                "missing_perspectives": ["Full critique unavailable"]
            },
            "improvements": [{
                "area": "Critique System",
                "suggestion": "Fix critique generation or use manual review",
                "priority": "high"
            }],
            "overall_quality": 5,
            "confidence_level": "low",
            "recommendation": "Use with caution and manual verification"
        }
    
    def display_critique(self, critique: Dict[str, Any]):
        """Display critique in readable format"""
        print("\n" + "="*60)
        print("🎯 CRITIQUE REPORT")
        print("="*60)
        print(f"Topic: {critique.get('topic', 'Unknown')}")
        
        # Validation scores
        validation = critique.get('validation', {})
        if validation:
            print(f"\n📊 VALIDATION SCORES:")
            print(f"   Completeness: {validation.get('completeness_score', 'N/A')}/10")
            print(f"   Accuracy: {validation.get('accuracy_score', 'N/A')}/10")
            print(f"   Source Credibility: {validation.get('source_credibility_score', 'N/A')}/10")
            
            if validation.get('biases_identified'):
                print(f"\n⚠️  Biases Identified:")
                for bias in validation['biases_identified'][:3]:  # Limit display
                    print(f"   • {bias}")
            
            if validation.get('assumptions'):
                print(f"\n🤔 Assumptions:")
                for assumption in validation['assumptions'][:3]:  # Limit display
                    print(f"   • {assumption}")
        
        # Critique details
        critique_details = critique.get('critique', {})
        if critique_details:
            print(f"\n📝 CRITIQUE:")
            
            if critique_details.get('strengths'):
                print(f"\n✅ Strengths:")
                for strength in critique_details['strengths'][:3]:
                    print(f"   • {strength}")
            
            if critique_details.get('weaknesses'):
                print(f"\n❌ Weaknesses:")
                for weakness in critique_details['weaknesses'][:3]:
                    print(f"   • {weakness}")
            
            if critique_details.get('logical_issues'):
                print(f"\n🔍 Logical Issues:")
                for issue in critique_details['logical_issues'][:3]:
                    print(f"   • {issue}")
            
            if critique_details.get('missing_perspectives'):
                print(f"\n👁️ Missing Perspectives:")
                for perspective in critique_details['missing_perspectives'][:3]:
                    print(f"   • {perspective}")
        
        # Improvements
        improvements = critique.get('improvements', [])
        if improvements:
            print(f"\n🚀 SUGGESTED IMPROVEMENTS:")
            for improvement in improvements[:3]:  # Limit display
                print(f"   • [{improvement.get('priority', 'medium').upper()}] {improvement.get('area')}:")
                print(f"     {improvement.get('suggestion', 'No suggestion')}")
        
        # Overall assessment
        print(f"\n📈 OVERALL ASSESSMENT:")
        print(f"   Quality Score: {critique.get('overall_quality', 'N/A')}/10")
        print(f"   Confidence: {critique.get('confidence_level', 'unknown').upper()}")
        print(f"   Recommendation: {critique.get('recommendation', 'No recommendation')}")


# Test the Critic Agent
if __name__ == "__main__":
    # First, let's load the test research from file
    try:
        with open("examples/test_research.json", "r") as f:
            test_research = json.load(f)
    except FileNotFoundError:
        print("Test research file not found. Creating sample research...")
        test_research = {
            "topic": "AI interview prep tools market in South Asia",
            "summary": "Sample research about AI interview tools",
            "key_findings": [
                {
                    "category": "Market Trends",
                    "points": ["Growing demand for AI interview tools", "Increased remote hiring"]
                }
            ],
            "sources": [
                {
                    "title": "Sample Source",
                    "url": "https://example.com",
                    "credibility": "medium"
                }
            ]
        }
    
    critic = CriticAgent()
    
    print("Testing Critic Agent...")
    print(f"Critiquing research on: {test_research.get('topic', 'Unknown topic')}")
    
    critique = critic.critique_research(test_research)
    critic.display_critique(critique)
    
    # Save critique to file
    with open("examples/test_critique.json", "w") as f:
        json.dump(critique, f, indent=2)
    print("\n✅ Critique saved to 'examples/test_critique.json'") 
