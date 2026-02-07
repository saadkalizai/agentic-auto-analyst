import os
from dotenv import load_dotenv

print("🧪 Simple Environment Test")
print("=" * 40)

# Load environment
load_dotenv()

# Check API key and model
api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL", "llama3-70b-8192")  # Default if not found

if api_key:
    print(f"✅ API Key: {api_key[:15]}...")
else:
    print("❌ No API Key found")

print(f"✅ Using Model: {model_name}")

# Test Groq connection
try:
    from langchain_groq import ChatGroq
    
    llm = ChatGroq(
        model=model_name,  # Use the model from .env file
        temperature=0.7,
        api_key=api_key  # Explicitly pass API key
    )
    
    # Simple test
    response = llm.invoke("Hello! Say 'Test successful' if you can read this.")
    print(f"✅ Groq Connection: {response.content[:50]}...")
    
except Exception as e:
    print(f"❌ Groq test failed: {e}")