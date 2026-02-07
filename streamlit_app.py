import streamlit as st
import json
import time
import os
from datetime import datetime
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .agent-card {
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1E88E5;
        background-color: #f8f9fa;
    }
    .success-card {
        border-left-color: #4CAF50;
        background-color: #f1f8e9;
    }
    .warning-card {
        border-left-color: #FF9800;
        background-color: #fff3e0;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Import mock system
try:
    from demo.mock_agents import MockAutoAnalyst
    from demo.mock_data import MockDataGenerator
    MOCK_AVAILABLE = True
except ImportError:
    MOCK_AVAILABLE = False

# Import real system
try:
    from app import AutoAnalyst
    REAL_AVAILABLE = True
except ImportError:
    REAL_AVAILABLE = False

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Auto-Analyst Settings")
    st.divider()
    
    # Mode selection
    st.subheader("Operation Mode")
    
    if not REAL_AVAILABLE and not MOCK_AVAILABLE:
        st.error("No analysis systems available. Please check imports.")
        mode = "demo"
    elif not REAL_AVAILABLE:
        st.warning("Real agent not available. Using demo mode only.")
        mode = "demo"
    else:
        mode = st.radio(
            "Select Mode:",
            ["Real Analysis", "Demo Mode"],
            help="Real: Uses actual web search and LLM. Demo: Uses mock data for fast testing."
        )
    
    st.divider()
    
    # Demo settings
    if mode == "Demo Mode" and MOCK_AVAILABLE:
        st.subheader("Demo Settings")
        
        speed = st.select_slider(
            "Simulation Speed:",
            options=["Fast", "Normal", "Realistic"],
            value="Normal",
            help="Fast: Quick demo, Normal: Realistic timing, Realistic: Simulates actual delays"
        )
        
        speed_map = {"Fast": "fast", "Normal": "normal", "Realistic": "realistic"}
        demo_speed = speed_map[speed]
        
        # Sample gallery
        st.subheader("Sample Gallery")
        generator = MockDataGenerator()
        samples = generator.get_sample_problems()
        
        for sample in samples:
            if st.button(f"📋 {sample['title']}", key=f"sample_{sample['id']}"):
                st.session_state.problem_input = sample['description']
                st.rerun()
    
    st.divider()
    
    # Export settings
    st.subheader("Export Options")
    export_format = st.radio(
        "Format:",
        ["JSON", "Text Summary", "Both"]
    )
    
    st.divider()
    st.caption("Auto-Analyst v1.0")
    st.caption(f"Mode: {'Real' if mode == 'Real Analysis' else 'Demo'}")

# Main content
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">🤖 AI Research & Decision-Making Agent</h1>', unsafe_allow_html=True)
with col2:
    st.metric("Analyses Run", len(st.session_state.analysis_history))

st.markdown("""
**Transform vague problems into research-backed insights** with sources, reasoning, and actionable recommendations.
""")

# Problem input
st.subheader("📝 Enter Your Problem or Query")

# Initialize problem input in session state
if 'problem_input' not in st.session_state:
    st.session_state.problem_input = "Analyze whether AI interview prep tools are a good startup idea in South Asia."

problem = st.text_area(
    " ",
    value=st.session_state.problem_input,
    height=150,
    placeholder="Example: 'Analyze the potential for renewable energy microgrids in rural Africa...'",
    label_visibility="collapsed"
)

# Quick example buttons
st.write("**Try these examples:**")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🚀 Startup Idea", use_container_width=True):
        st.session_state.problem_input = "Analyze whether AI interview prep tools are a good startup idea in South Asia."
        st.rerun()
with col2:
    if st.button("📈 Market Analysis", use_container_width=True):
        st.session_state.problem_input = "Analyze the electric vehicle market growth potential in Southeast Asia."
        st.rerun()
with col3:
    if st.button("🏥 Healthcare Tech", use_container_width=True):
        st.session_state.problem_input = "Evaluate the adoption of AI in healthcare diagnosis in developing countries."
        st.rerun()
with col4:
    if st.button("🍔 Food Delivery", use_container_width=True):
        st.session_state.problem_input = "Analyze the potential for a food delivery app in rural areas with limited infrastructure."
        st.rerun()

# Analysis button
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "🚀 START ANALYSIS",
        type="primary",
        use_container_width=True,
        disabled=(not REAL_AVAILABLE and not MOCK_AVAILABLE)
    )

# Agent visualization placeholder
agent_placeholder = st.empty()
results_placeholder = st.empty()

# Analysis execution
if analyze_button and problem:
    with agent_placeholder.container():
        st.subheader("🔍 Analysis Progress")
        
        # Create progress tracker
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Agent visualization
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            agent1 = st.container()
            agent1.markdown('<div class="agent-card">', unsafe_allow_html=True)
            agent1.markdown("**📋 Task Planner**")
            agent1.markdown("Breaking down problem...")
            agent1.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            agent2 = st.container()
            agent2.markdown('<div class="agent-card">', unsafe_allow_html=True)
            agent2.markdown("**🔍 Researcher**")
            agent2.markdown("Waiting...")
            agent2.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            agent3 = st.container()
            agent3.markdown('<div class="agent-card">', unsafe_allow_html=True)
            agent3.markdown("**🎯 Critic**")
            agent3.markdown("Waiting...")
            agent3.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            agent4 = st.container()
            agent4.markdown('<div class="agent-card">', unsafe_allow_html=True)
            agent4.markdown("**📄 Reporter**")
            agent4.markdown("Waiting...")
            agent4.markdown('</div>', unsafe_allow_html=True)
        
        # Run analysis based on mode
        try:
            if mode == "Real Analysis" and REAL_AVAILABLE:
                # Real analysis
                status_text.text("Initializing real agents...")
                progress_bar.progress(10)
                time.sleep(1)
                
                analyst = AutoAnalyst()
                
                status_text.text("📋 Planning tasks...")
                progress_bar.progress(30)
                agent1.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent1.markdown("**📋 Task Planner**")
                agent1.markdown("✅ Planning complete")
                agent1.markdown('</div>', unsafe_allow_html=True)
                time.sleep(1)
                
                status_text.text("🔍 Researching web...")
                progress_bar.progress(50)
                agent2.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent2.markdown("**🔍 Researcher**")
                agent2.markdown("✅ Researching...")
                agent2.markdown('</div>', unsafe_allow_html=True)
                time.sleep(2)
                
                status_text.text("🎯 Critical analysis...")
                progress_bar.progress(70)
                agent3.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent3.markdown("**🎯 Critic**")
                agent3.markdown("✅ Validating...")
                agent3.markdown('</div>', unsafe_allow_html=True)
                time.sleep(1)
                
                status_text.text("📄 Generating final report...")
                progress_bar.progress(90)
                agent4.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent4.markdown("**📄 Reporter**")
                agent4.markdown("✅ Compiling...")
                agent4.markdown('</div>', unsafe_allow_html=True)
                
                # Run actual analysis
                report = analyst.analyze(problem)
                
                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)
                
            else:
                # Demo mode
                status_text.text("Starting demo analysis...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                analyst = MockAutoAnalyst(speed=demo_speed if 'demo_speed' in locals() else "normal")
                
                status_text.text("📋 Planning tasks...")
                progress_bar.progress(40)
                agent1.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent1.markdown("**📋 Task Planner**")
                agent1.markdown("✅ Mock planning complete")
                agent1.markdown('</div>', unsafe_allow_html=True)
                time.sleep(1 * (0.5 if demo_speed == "fast" else 1.0))
                
                status_text.text("🔍 Simulating research...")
                progress_bar.progress(60)
                agent2.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent2.markdown("**🔍 Researcher**")
                agent2.markdown("✅ Mock data generated")
                agent2.markdown('</div>', unsafe_allow_html=True)
                time.sleep(1.5 * (0.5 if demo_speed == "fast" else 1.0))
                
                status_text.text("🎯 Critical analysis...")
                progress_bar.progress(80)
                agent3.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent3.markdown("**🎯 Critic**")
                agent3.markdown("✅ Mock critique done")
                agent3.markdown('</div>', unsafe_allow_html=True)
                time.sleep(1 * (0.5 if demo_speed == "fast" else 1.0))
                
                status_text.text("📄 Generating report...")
                progress_bar.progress(95)
                agent4.markdown('<div class="agent-card success-card">', unsafe_allow_html=True)
                agent4.markdown("**📄 Reporter**")
                agent4.markdown("✅ Report ready")
                agent4.markdown('</div>', unsafe_allow_html=True)
                time.sleep(0.5)
                
                # Run mock analysis
                result = analyst.analyze(problem)
                report = result['final_report']
                
                status_text.text("✅ Demo analysis complete!")
                progress_bar.progress(100)
            
            # Store in history
            analysis_entry = {
                "timestamp": datetime.now().isoformat(),
                "problem": problem[:100] + "..." if len(problem) > 100 else problem,
                "mode": mode,
                "report": report
            }
            st.session_state.analysis_history.insert(0, analysis_entry)
            st.session_state.current_analysis = report
            
            # Show success
            time.sleep(0.5)
            st.success(f"Analysis complete! Generated report with {len(report.get('recommendations', []))} recommendations.")
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.info("Try switching to Demo Mode or check your API configuration.")

# Display results if available
if st.session_state.current_analysis:
    with results_placeholder.container():
        st.divider()
        st.subheader("📊 Analysis Results")
        
        report = st.session_state.current_analysis
        exec_summary = report.get('executive_summary', {})
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Quality Score", f"{exec_summary.get('overall_quality_score', 'N/A')}/10")
        with col2:
            st.metric("Confidence", exec_summary.get('confidence_level', 'N/A').upper())
        with col3:
            st.metric("Recommendations", len(report.get('recommendations', [])))
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Executive Summary", "🎯 Recommendations", "🚀 Next Steps", "📁 Export"])
        
        with tab1:
            st.write("**Problem Statement:**")
            st.info(exec_summary.get('problem_statement', 'No problem statement'))
            
            st.write("**Key Insights:**")
            for insight in exec_summary.get('key_insights', []):
                st.markdown(f"• {insight}")
            
            st.write("**Overall Assessment:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Quality:** {exec_summary.get('overall_quality_score', 'N/A')}/10")
            with col2:
                st.write(f"**Confidence:** {exec_summary.get('confidence_level', 'N/A').upper()}")
        
        with tab2:
            st.write("**Actionable Recommendations:**")
            for i, rec in enumerate(report.get('recommendations', []), 1):
                st.markdown(f"{i}. **{rec}**")
        
        with tab3:
            st.write("**Suggested Next Steps:**")
            for i, step in enumerate(report.get('next_steps', []), 1):
                st.markdown(f"{i}. {step}")
        
        with tab4:
            st.write("**Export Options**")
            
            if export_format in ["JSON", "Both"]:
                json_str = json.dumps(report, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"auto_analyst_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            if export_format in ["Text Summary", "Both"]:
                # Create text summary
                text_summary = f"""AUTO-ANALYST REPORT
{'='*50}
Problem: {exec_summary.get('problem_statement', '')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Mode: {mode}

EXECUTIVE SUMMARY:
{'='*30}
Overall Quality: {exec_summary.get('overall_quality_score', 'N/A')}/10
Confidence: {exec_summary.get('confidence_level', 'N/A').upper()}

KEY INSIGHTS:
"""
                for insight in exec_summary.get('key_insights', []):
                    text_summary += f"• {insight}\n"
                
                text_summary += f"\nRECOMMENDATIONS:\n{'='*30}\n"
                for i, rec in enumerate(report.get('recommendations', []), 1):
                    text_summary += f"{i}. {rec}\n"
                
                st.download_button(
                    label="📄 Download Text Summary",
                    data=text_summary,
                    file_name=f"auto_analyst_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
            st.info("Reports are also automatically saved to the 'outputs/' folder.")

# History panel
if st.session_state.analysis_history:
    with st.sidebar:
        st.divider()
        st.subheader("📜 Analysis History")
        
        for i, entry in enumerate(st.session_state.analysis_history[:5]):
            with st.expander(f"{entry['timestamp'][11:16]} - {entry['problem']}"):
                st.caption(f"Mode: {entry['mode']}")
                if st.button("Load", key=f"load_{i}"):
                    st.session_state.current_analysis = entry['report']
                    st.rerun()

# Footer
st.divider()
st.caption("Built with LangChain, Groq LLM, and Streamlit | Auto-Analyst v1.0") 
