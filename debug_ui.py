 
import streamlit as st
import os
from dotenv import load_dotenv

# Simulate what Streamlit does
load_dotenv()

print("🔍 Debugging UI Data Flow")
print("="*60)

# Check API keys
print(f"1. API Keys loaded:")
print(f"   GROQ_API_KEY: {bool(os.getenv('GROQ_API_KEY'))}")
print(f"   SERP_API_KEY: {bool(os.getenv('SERP_API_KEY'))}")

# Check imports
try:
    from app import AutoAnalyst
    print("2. ✅ AutoAnalyst import successful")
    
    # Run a test
    print("3. Running test analysis...")
    analyst = AutoAnalyst()
    report = analyst.analyze("test query about germany vs italy")
    
    print(f"4. Report generated:")
    print(f"   Quality score: {report.get('executive_summary', {}).get('overall_quality_score', 'MISSING')}")
    print(f"   Recommendations: {len(report.get('recommendations', []))}")
    
    # Check what's actually in the report
    if 'executive_summary' in report:
        print(f"\n5. Executive summary exists with data")
    else:
        print(f"\n5. ❌ NO executive_summary in report")
        print(f"   Report keys: {report.keys()}")
        
except Exception as e:
    print(f"❌ Error: {e}")