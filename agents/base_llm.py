import os
from typing import Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class BaseLLM:
    """Base LLM wrapper for Groq API"""
    
    def __init__(self, model: Optional[str] = None, temperature: float = 0.7):
        """
        Initialize the LLM with Groq
        
        Args:
            model: Groq model name (defaults to .env or llama-3.3-70b-versatile)
            temperature: Creativity level (0.0 to 1.0)
        """
        import streamlit as st
        self.api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        self.model = model or st.secrets.get("GROQ_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key
        )
    
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error generating response: {e}"
    
    def __call__(self, prompt: str) -> str:
        """Make the class callable for convenience"""
        return self.generate(prompt)


# Test the class
if __name__ == "__main__":
    llm = BaseLLM()
    test_response = llm("What is 2+2? Answer in one word.")
    print("Test response:", test_response) 
