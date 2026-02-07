 
"## ?? Overview" 
"An autonomous agent that takes vague problems and turns them into research-backed insights with sources, reasoning, and action steps." 
 
"## ?? Features" 
"- ?? **Multi-Agent System**: Planner, Researcher, Critic, Reporter" 
"- ?? **Real Web Search**: SERP API (Google Search) integration" 
"- ?? **LLM Analysis**: Groq with LLaMA/Mistral models" 
"- ?? **Critical Validation**: Quality scoring and bias detection" 
"- ?? **Web Interface**: Streamlit UI with Demo/Real modes" 
 
"## ??? Installation" 
"\`\`\`bash" 
"# Clone repository" 
"git clone https://github.com/saadkalizai/agentic-auto-analyst.git" 
"cd agentic-auto-analyst" 
 
"# Create virtual environment" 
"python -m venv venv" 
"venv\Scripts\activate  # Windows" 
"# source venv/bin/activate  # Mac/Linux" 
 
"# Install dependencies" 
"pip install -r requirements.txt" 
"\`\`\`" 
 
"## ?? Configuration" 
"1. Get free API keys:" 
"   - [Groq API](https://console.groq.com)" 
"   - [SERP API](https://serpapi.com)" 
"2. Create \`.env\` file:" 
"\`\`\`env" 
"GROQ_API_KEY=your_groq_key" 
"GROQ_MODEL=llama-3.3-70b-versatile" 
"SERP_API_KEY=your_serpapi_key" 
"\`\`\`" 
 
"## ?? Usage" 
 
"### Command Line" 
"\`\`\`bash" 
"# Run analysis" 
"python app.py" 
 
"# Run specific agent test" 
"python agents/researcher.py" 
"python agents/planner.py" 
"\`\`\`" 
 
"### Web Interface" 
"\`\`\`bash" 
"streamlit run streamlit_app.py" 
"# Open http://localhost:8501" 
"\`\`\`" 
 
"## ?? Example Queries" 
"- \"Analyze whether AI interview prep tools are a good startup idea in South Asia\"" 
"- \"Should I pursue a Masters in Data Science after AI Bachelor's?\"" 
"- \"Evaluate electric vehicle market growth potential in Southeast Asia\"" 
