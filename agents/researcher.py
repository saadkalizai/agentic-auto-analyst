import json
import os
from typing import List, Dict, Any
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from agents.base_llm import BaseLLM

load_dotenv()

class ResearchAgent:
    """Agent that performs web research using SERP API (Google Search)"""
    
    def __init__(self, model: str = None, temperature: float = 0.7):
        """
        Initialize the Research Agent
        
        Args:
            model: LLM model to use
            temperature: Creativity level for analysis
        """
        self.llm = BaseLLM(model=model, temperature=temperature)
        import streamlit as st
        self.serp_api_key = st.secrets.get("SERP_API_KEY", os.getenv("SERP_API_KEY"))
        
        # Research prompt template
        self.research_prompt = """You are an expert research analyst. Analyze the provided search results and create a comprehensive summary.

RESEARCH TOPIC: {topic}

SEARCH RESULTS:
{search_results}

INSTRUCTIONS:
1. Extract key insights from the search results
2. Identify trends, statistics, and important facts
3. Note any contradictions or gaps in information
4. Organize findings into logical categories
5. Include source credibility assessment
6. If the topic is about career choices or education decisions, provide comparative analysis with pros/cons
7. Output in JSON format:
{{
    "topic": "Research topic",
    "summary": "Concise overview of findings",
    "key_findings": [
        {{
            "category": "Category name",
            "points": ["point 1", "point 2", ...]
        }}
    ],
    "statistics": ["stat 1", "stat 2", ...],
    "sources": [
        {{
            "title": "Source title",
            "url": "Source URL",
            "credibility": "high/medium/low"
        }}
    ],
    "gaps": ["What information is missing"],
    "next_steps": ["Recommended follow-up research"]
}}

OUTPUT ONLY VALID JSON:"""
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web using SERP API (Google Search)
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        if not self.serp_api_key:
            print("❌ SERP_API_KEY not found in environment variables")
            return self._fallback_search(query, max_results)
        
        try:
            from serpapi import GoogleSearch
            
            # Use simple optimization
            optimized_query = self._optimize_query(query)
            # If query is too long, use first 10 words
            if len(optimized_query.split()) > 15:
                optimized_query = " ".join(optimized_query.split()[:12])
            print(f"🔍 Searching: {optimized_query[:80]}...")
            
            params = {
                "q": optimized_query,
                "api_key": self.serp_api_key,
                "num": max_results,
                "engine": "google"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            search_results = []
            if "organic_results" in results:
                for item in results["organic_results"][:max_results]:
                    search_results.append({
                        "title": item.get("title", ""),
                        "snippet": item.get("snippet", ""),
                        "url": item.get("link", "")
                    })
            
            print(f"✅ Found {len(search_results)} results")
            return search_results
            
        except Exception as e:
            print(f"❌ SERP API error: {e}")
            return self._fallback_search(query, max_results)
    
    def _fallback_search(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Fallback search using DuckDuckGo"""
        try:
            print(f"🔄 Trying DuckDuckGo fallback: {query}")
            from duckduckgo_search import DDGS
            ddgs = DDGS()
            
            results = []
            search_gen = ddgs.text(query, max_results=max_results)
            
            for result in search_gen:
                results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("body", ""),
                    "url": result.get("href", "")
                })
            
            print(f"✅ Fallback found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Fallback search failed: {e}")
            return []
    
    def _optimize_query(self, query: str) -> str:
        """Simple universal query optimizer"""
        # Keep original query exactly as user typed
        # Just add year for recency
        
        query_lower = query.lower().strip()
        
        # Only add 2024 if not already present
        if "2024" not in query_lower and "2023" not in query_lower:
            return f"{query} 2024"
        
        return query  # Return original unchanged
    
    def format_search_results(self, results: List[Dict[str, str]]) -> str:
        """Format search results for the LLM prompt"""
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"RESULT {i}:")
            formatted.append(f"Title: {result['title']}")
            formatted.append(f"Snippet: {result['snippet'][:300]}...")
            formatted.append(f"URL: {result['url']}")
            formatted.append("---")
        
        return "\n".join(formatted)
    
    def research_topic(self, topic: str, search_query: str = None) -> Dict[str, Any]:
        """
        Research a topic and return analyzed results
        
        Args:
            topic: The topic to research
            search_query: Optional custom search query (defaults to topic)
            
        Returns:
            Analyzed research results
        """
        # Use topic as search query if none provided
        query = search_query or topic
        
        print(f"📚 Researching topic: {topic}")
        
        # Perform web search
        search_results = self.search_web(query)
        
        if not search_results:
            print("⚠️ No search results found")
            return self._create_empty_research(topic)
        
        print(f"✅ Processing {len(search_results)} search results")
        
        # Format results for LLM
        formatted_results = self.format_search_results(search_results)
        
        # Create prompt
        prompt = self.research_prompt.format(
            topic=topic,
            search_results=formatted_results
        )
        
        try:
            # Get analysis from LLM
            response = self.llm(prompt)
            
            # Extract JSON
            json_str = self._extract_json(response)
            
            # Parse JSON
            research = json.loads(json_str)
            
            # Add raw search results
            research["raw_results"] = search_results
            
            return research
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return self._create_basic_research(topic, search_results)
    
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
                "summary": "Could not parse LLM response",
                "key_findings": [],
                "statistics": [],
                "sources": [],
                "gaps": ["Could not parse analysis"],
                "next_steps": ["Retry research"]
            })
    
    def _create_empty_research(self, topic: str) -> Dict[str, Any]:
        """Create empty research structure"""
        return {
            "topic": topic,
            "summary": "No search results found",
            "key_findings": [],
            "statistics": [],
            "sources": [],
            "gaps": ["No information available from search"],
            "next_steps": ["Try different search terms", "Check internet connection"],
            "raw_results": []
        }
    
    def _create_basic_research(self, topic: str, search_results: List[Dict]) -> Dict[str, Any]:
        """Create basic research structure from raw results"""
        return {
            "topic": topic,
            "summary": f"Found {len(search_results)} results but analysis failed",
            "key_findings": [
                {
                    "category": "Raw Search Results",
                    "points": [f"{r['title'][:100]}..." for r in search_results[:3]]
                }
            ],
            "statistics": [f"Total results: {len(search_results)}"],
            "sources": [
                {
                    "title": r["title"],
                    "url": r["url"],
                    "credibility": "unknown"
                }
                for r in search_results[:3]
            ],
            "gaps": ["LLM analysis unavailable"],
            "next_steps": ["Manual analysis required"],
            "raw_results": search_results
        }
    
    def display_research(self, research: Dict[str, Any]):
        """Display research results in readable format"""
        print("\n" + "="*60)
        print("🔬 RESEARCH REPORT")
        print("="*60)
        print(f"Topic: {research['topic']}")
        print(f"\n📋 Summary: {research['summary']}")
        
        if research['key_findings']:
            print("\n📊 Key Findings:")
            print("-"*60)
            for finding in research['key_findings']:
                print(f"\n📌 {finding['category']}:")
                for point in finding['points']:
                    print(f"   • {point}")
        
        if research['statistics']:
            print(f"\n📈 Statistics:")
            for stat in research['statistics']:
                print(f"   • {stat}")
        
        if research['sources']:
            print(f"\n📚 Sources ({len(research['sources'])}):")
            for source in research['sources'][:3]:
                print(f"   • {source['title'][:80]}... ({source['credibility']})")
        
        if research['gaps']:
            print(f"\n⚠️  Information Gaps:")
            for gap in research['gaps']:
                print(f"   • {gap}")
        
        if research['next_steps']:
            print(f"\n🚀 Next Steps:")
            for step in research['next_steps']:
                print(f"   • {step}")
        
        print(f"\n📊 Raw results: {len(research.get('raw_results', []))} items")


# Test the Research Agent
if __name__ == "__main__":
    researcher = ResearchAgent()
    
    # Test with a sample topic
    test_topic = "Masters in data science career prospects 2024"
    
    print("🧪 Testing Research Agent with SERP API")
    print("="*60)
    print(f"Topic: {test_topic}")
    
    research = researcher.research_topic(test_topic)
    researcher.display_research(research)
    
    # Save research to file
    os.makedirs("examples", exist_ok=True)
    with open("examples/test_research_serp.json", "w") as f:
        json.dump(research, f, indent=2)
    print("\n✅ Research saved to 'examples/test_research_serp.json'")