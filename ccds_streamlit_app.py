import streamlit as st
import pandas as pd
from corrosion_engine import CorrosionEngine
from document_processor import DocumentProcessor
from report_generator import ReportGenerator
import random

# Page config
st.set_page_config(
    page_title="CCDs Simulation Auditor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e293b 0%, #1e40af 50%, #1e293b 100%);
    }
    .stAlert {
        border-radius: 10px;
    }
    h1 {
        color: #60a5fa;
        text-align: center;
    }
    h2, h3 {
        color: #93c5fd;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("⚡ CCDs Simulation Auditor")
st.markdown("### Physics-Informed AI for Corrosion Control Document Validation")
st.markdown("**Extract • Simulate • Verify • Predict**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")
    
    mode = st.radio(
        "Select Mode:",
        ["Upload Document", "Generate Sample Document", "About"]
    )
    
    st.divider()
    
    if mode == "Upload Document":
        st.info("📄 Upload a CCD text file or paste content directly")
    elif mode == "Generate Sample Document":
        st.info("🎲 Generate random CCD for testing")
    else:
        st.info("ℹ️ Learn about the system")

# About Section
if mode == "About":
    st.header("About CCDs Simulation Auditor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 What It Does")
        st.markdown("""
        This tool performs simulation-based audits of Corrosion Control Documents:
        
        1. **Extracts Parameters**: Uses NLP to read CCDs and extract critical specifications
        2. **Runs Simulations**: Applies empirical corrosion rate models
        3. **Identifies Gaps**: Compares predicted vs required design life
        4. **Generates Insights**: Provides actionable engineering recommendations
        """)
    
    with col2:
        st.subheader("🔧 How to Use")
        st.markdown("""
        **Option 1: Upload Document**
        - Upload a .txt file containing your CCD
        - Or paste the content directly
        - Click "Run Simulation"
        
        **Option 2: Generate Sample**
        - Select risk level (Critical/Moderate/Acceptable)
        - Generate random CCD with realistic parameters
        - Experiment and learn!
        """)
    
    st.divider()
    
    st.subheader("📊 Technical Details")
    st.markdown("""
    **Corrosion Rate Model**: Based on NACE/API standards
    
    - Considers material type, coating, environment
    - Temperature correction (Arrhenius-based)
    - H₂S partial pressure effects
    - Coating effectiveness factors
    
    **Risk Levels**:
    - 🔴 **Critical**: Failure before design life
    - 🟠 **High**: < 20% safety margin
    - 🟡 **Moderate**: < 50% safety margin
    - 🟢 **Low**: Adequate design
    """)

# Generate Sample Document
elif mode == "Generate Sample Document":
    st.header("🎲 Generate Sample CCD")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        risk_level = st.selectbox(
            "Select Risk Level for Sample:",
            ["Critical (High Risk)", "Moderate Risk", "Acceptable (Low Risk)"]
        )
    
    with col2:
        if st.button("🎲 Generate Random CCD", type="primary", use_container_width=True):
            # Generate based on risk level
            if "Critical" in risk_level:
                sample = DocumentProcessor.generate_sample_document("critical")
            elif "Moderate" in risk_level:
                sample = DocumentProcessor.generate_sample_document("moderate")
            else:
                sample = DocumentProcessor.generate_sample_document("acceptable")
            
            st.session_state['generated_doc'] = sample
            st.session_state['doc_generated'] = True
            st.rerun()
    
    # Display generated document
    if st.session_state.get('doc_generated', False):
        st.subheader("📄 Generated Document")
        
        doc_content = st.text_area(
            "Document Content (editable):",
            value=st.session_state.get('generated_doc', ''),
            height=400,
            key="generated_content"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("▶️ Run Simulation on This Document", type="primary", use_container_width=True):
                st.session_state['document'] = doc_content
                st.session_state['run_simulation'] = True
                st.rerun()
        
        with col2:
            if st.button("💾 Download Document", use_container_width=True):
                st.download_button(
                    label="Download as TXT",
                    data=doc_content,
                    file_name="sample_ccd.txt",
                    mime="text/plain"
                )

# Upload Document
elif mode == "Upload Document":
    st.header("📄 Document Input")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload CCD Document (.txt file)",
        type=['txt'],
        help="Upload a text file containing your Corrosion Control Document"
    )
    
    # Text area for pasting
    st.subheader("Or Paste Content Directly")
    doc_text = st.text_area(
        "Paste your CCD content here:",
        height=300,
        placeholder="""Example CCD format:

CORROSION CONTROL DOCUMENT - Pipeline Section A-102

Material: Carbon Steel API 5L X65
Coating: 3-layer Polyethylene (3LPE)
Environment: Sour gas service with H2S
Design Life: 25 years
Wall Thickness: 12.7 mm
Minimum Acceptable Thickness: 6.0 mm
Operating Temperature: 60°C
Pressure: 70 bar
"""
    )
    
    # Determine document content
    document_content = ""
    if uploaded_file is not None:
        document_content = uploaded_file.read().decode('utf-8')
        st.success(f"✅ File uploaded: {uploaded_file.name}")
    elif doc_text.strip():
        document_content = doc_text
    
    # Run simulation button
    if document_content:
        if st.button("▶️ Run Simulation Audit", type="primary", use_container_width=True):
            st.session_state['document'] = document_content
            st.session_state['run_simulation'] = True
            st.rerun()
    else:
        st.info("👆 Please upload a file or paste document content to continue")

# Run Simulation and Show Results
if st.session_state.get('run_simulation', False):
    st.divider()
    st.header("📊 Simulation Results")
    
    document = st.session_state.get('document', '')
    
    with st.spinner("🔄 Extracting parameters and running simulation..."):
        # Extract parameters
        params = DocumentProcessor.extract_parameters(document)
        
        # Calculate corrosion
        results = CorrosionEngine.calculate_corrosion(params)
        
        # Generate report
        report = ReportGenerator.generate_report(params, results)
    
    # Risk Alert Box
    risk_colors = {
        'critical': ('🔴', '#ff4444', '#ffcccc'),
        'high': ('🟠', '#ff8800', '#ffe0cc'),
        'moderate': ('🟡', '#ffcc00', '#fff5cc'),
        'low': ('🟢', '#00cc44', '#ccffdd')
    }
    
    icon, color, bg = risk_colors.get(report['risk_level'], ('⚪', '#888888', '#eeeeee'))
    
    st.markdown(f"""
    <div style='background-color: {bg}; border: 3px solid {color}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
        <h2 style='color: {color}; margin: 0;'>{icon} {report['risk_level'].upper()} RISK LEVEL</h2>
        <p style='font-size: 18px; margin: 10px 0; color: #333;'>{report['risk_message']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Design Life", f"{params['design_life']} years")
    
    with col2:
        st.metric(
            "Predicted Life", 
            f"{results['time_to_failure']:.1f} years",
            delta=f"{results['time_to_failure'] - params['design_life']:.1f} years"
        )
    
    with col3:
        st.metric("Corrosion Rate", f"{results['corrosion_rate']:.3f} mm/yr")
    
    with col4:
        st.metric("Safety Margin", f"{((results['time_to_failure']/params['design_life'] - 1) * 100):.1f}%")
    
    st.divider()
    
    # Extracted Parameters
    st.subheader("🔍 Extracted Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        param_df = pd.DataFrame({
            'Parameter': ['Material', 'Coating', 'Environment', 'Temperature'],
            'Value': [
                params['material'].replace('_', ' ').title(),
                params['coating'].replace('_', ' ').title(),
                params['environment'].replace('_', ' ').title(),
                f"{params['temperature']}°C"
            ],
            'Confidence': [
                f"{params['confidence'].get('material', 0)*100:.0f}%",
                f"{params['confidence'].get('coating', 0)*100:.0f}%",
                f"{params['confidence'].get('environment', 0)*100:.0f}%",
                f"{params['confidence'].get('temperature', 0)*100:.0f}%"
            ]
        })
        st.dataframe(param_df, use_container_width=True, hide_index=True)
    
    with col2:
        dimension_df = pd.DataFrame({
            'Parameter': ['Initial Thickness', 'Min Thickness', 'Design Life', 'H₂S Pressure'],
            'Value': [
                f"{params['initial_thickness']} mm",
                f"{params['min_thickness']} mm",
                f"{params['design_life']} years",
                f"{params['h2s_pressure']} bar"
            ]
        })
        st.dataframe(dimension_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Chart
    st.subheader("📉 Wall Thickness Degradation Over Time")
    
    chart_data = pd.DataFrame(results['time_series'])
    chart_data = chart_data.rename(columns={
        'year': 'Year',
        'thickness': 'Predicted Thickness (mm)'
    })
    
    st.line_chart(chart_data, x='Year', y='Predicted Thickness (mm)', use_container_width=True)
    
    # Add reference lines info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"🟡 Design Life: {params['design_life']} years")
    with col2:
        st.error(f"🔴 Min Thickness: {params['min_thickness']} mm")
    with col3:
        st.warning(f"⚠️ Predicted Failure: {results['time_to_failure']:.1f} years")
    
    st.divider()
    
    # Recommendations
    st.subheader("💡 Engineering Recommendations")
    
    for rec in report['recommendations']:
        priority_colors = {
            'URGENT': ('🔴', '#ff4444'),
            'HIGH': ('🟠', '#ff8800'),
            'MEDIUM': ('🟡', '#ffcc00'),
            'LOW': ('🟢', '#00cc44')
        }
        
        icon, color = priority_colors.get(rec['priority'], ('⚪', '#888888'))
        
        with st.expander(f"{icon} **{rec['priority']}** - {rec['category']}", expanded=(rec['priority'] in ['URGENT', 'HIGH'])):
            st.markdown(f"**Recommendation:** {rec['recommendation']}")
            st.markdown(f"**Impact:** {rec['impact']}")
    
    st.divider()
    
    # Download Report
    col1, col2 = st.columns([1, 4])
    with col1:
        report_text = ReportGenerator.generate_text_report(params, results, report)
        st.download_button(
            label="📥 Download Full Report",
            data=report_text,
            file_name="ccd_audit_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Run New Simulation", use_container_width=True):
            st.session_state['run_simulation'] = False
            st.session_state['document'] = ''
            st.rerun()

# Initialize session state
if 'run_simulation' not in st.session_state:
    st.session_state['run_simulation'] = False
if 'document' not in st.session_state:
    st.session_state['document'] = ''
