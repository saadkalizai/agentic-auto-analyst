import json
import os

# List all report files
files = os.listdir('outputs')
final_reports = [f for f in files if 'final_report' in f]

if not final_reports:
    print("❌ No final reports found")
    exit()

# Get latest
latest = max(final_reports)
print(f"📁 Latest report: {latest}")

# Load and inspect
with open(f'outputs/{latest}', 'r') as f:
    data = json.load(f)

print("\n🔍 Report Structure:")
print(f"Keys: {list(data.keys())}")

if 'executive_summary' in data:
    print(f"\n📊 Executive Summary:")
    print(f"  Quality score: {data['executive_summary'].get('overall_quality_score', 'MISSING')}")
    print(f"  Confidence: {data['executive_summary'].get('confidence_level', 'MISSING')}")
    print(f"  Recommendations count: {len(data.get('recommendations', []))}")
    
    # Show full executive summary
    print(f"\n📋 Full executive_summary:")
    print(json.dumps(data['executive_summary'], indent=2))
else:
    print("❌ NO executive_summary in report") 
