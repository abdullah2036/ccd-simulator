import streamlit as st
import pandas as pd
from corrosion_engine import CorrosionEngine
from document_processor import DocumentProcessor
from report_generator import ReportGenerator

# Page config
st.set_page_config(
    page_title="CCDs Simulation Auditor - Enhanced",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .financial-box {
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #10b981;
        margin: 10px 0;
    }
    .ml-badge {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("⚡ CCDs Simulation Auditor - Enhanced")
st.markdown("### Hybrid Physics-ML Engine with Financial Impact Analysis")
st.markdown("**Extract • Simulate • Verify • Predict • Quantify**")

# Feature badges
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="ml-badge">🤖 ML-ENHANCED</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="ml-badge">💰 FINANCIAL ROI</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="ml-badge">🔒 OFFLINE MODE</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="ml-badge">📊 BUSINESS CASE</div>', unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")
    
    mode = st.radio(
        "Select Mode:",
        ["Upload Document", "Generate Sample Document", "About", "Advanced Settings"]
    )
    
    st.divider()
    
    # Advanced Settings
    if mode == "Advanced Settings":
        st.subheader("⚙️ Configuration")
        
        use_ml = st.checkbox("Enable ML Enhancement", value=True, 
                            help="Use Machine Learning to refine predictions")
        
        offline_mode = st.checkbox("Offline Mode", value=True,
                                  help="Use only local resources (no internet)")
        
        use_local_llm = st.checkbox("Local LLM Processing", value=False,
                                    help="Use local transformer models (requires transformers library)")
        
        st.divider()
        st.subheader("💰 Financial Parameters")
        
        pipeline_length = st.number_input("Pipeline Length (m)", value=1000, min_value=1)
        surface_area = st.number_input("Surface Area (m²)", value=1000, min_value=1)
        
        st.session_state['use_ml'] = use_ml
        st.session_state['offline_mode'] = offline_mode
        st.session_state['use_local_llm'] = use_local_llm
        st.session_state['pipeline_length'] = pipeline_length
        st.session_state['surface_area'] = surface_area
    else:
        # Set defaults if not configured
        if 'use_ml' not in st.session_state:
            st.session_state['use_ml'] = True
        if 'offline_mode' not in st.session_state:
            st.session_state['offline_mode'] = True
        if 'use_local_llm' not in st.session_state:
            st.session_state['use_local_llm'] = False
        if 'pipeline_length' not in st.session_state:
            st.session_state['pipeline_length'] = 1000
        if 'surface_area' not in st.session_state:
            st.session_state['surface_area'] = 1000
    
    if mode == "Upload Document":
        st.info("📄 Upload a CCD text file or paste content")
    elif mode == "Generate Sample Document":
        st.info("🎲 Generate random CCD for testing")
    elif mode == "About":
        st.info("ℹ️ Learn about the enhanced system")

# About Section
if mode == "About":
    st.header("About CCDs Simulation Auditor - Enhanced Edition")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Core Capabilities")
        st.markdown("""
        **1. Hybrid Physics-ML Engine**
        - Combines empirical corrosion models with Machine Learning
        - ML refines predictions based on interacting variables
        - Provides confidence scores for transparency
        
        **2. Financial Impact Analysis**
        - Calculates Cost of Failure (CoF)
        - Quantifies ROI for design improvements
        - Provides business case justification
        
        **3. Offline Operation**
        - Works without internet connectivity
        - Optional local LLM for document processing
        - Ideal for remote sites and confidential data
        
        **4. Advanced Recommendations**
        - Engineering solutions with financial metrics
        - Payback period and NPV calculations
        - Risk-based prioritization
        """)
    
    with col2:
        st.subheader("🔬 Technical Innovation")
        st.markdown("""
        **Machine Learning Component:**
        - Random Forest model trained on synthetic corrosion data
        - Predicts correction factors for empirical formulas
        - Accounts for complex variable interactions
        - Auto-trains on first run (no setup required)
        
        **Financial Module:**
        - Industry-standard cost parameters
        - Downtime and repair cost estimation
        - Environmental and regulatory cost factors
        - ROI analysis for material upgrades
        
        **Privacy & Security:**
        - All processing happens locally
        - No data leaves your device
        - Optional offline LLM (requires transformers)
        - Suitable for confidential engineering documents
        """)
    
    st.divider()
    st.subheader("📊 What Makes This Special?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Innovation", "High", delta="Multi-layer AI")
    with col2:
        st.metric("Business Impact", "Quantified", delta="ROI Analysis")
    with col3:
        st.metric("Practical Deployment", "Ready", delta="Offline Capable")

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
            if "Critical" in risk_level:
                sample = DocumentProcessor.generate_sample_document("critical")
            elif "Moderate" in risk_level:
                sample = DocumentProcessor.generate_sample_document("moderate")
            else:
                sample = DocumentProcessor.generate_sample_document("acceptable")
            
            st.session_state['generated_doc'] = sample
            st.session_state['doc_generated'] = True
            st.rerun()
    
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
            st.download_button(
                label="💾 Download Document",
                data=doc_content,
                file_name="sample_ccd.txt",
                mime="text/plain",
                use_container_width=True
            )

# Upload Document
elif mode == "Upload Document":
    st.header("📄 Document Input")
    
    uploaded_file = st.file_uploader(
        "Upload CCD Document (.txt file)",
        type=['txt'],
        help="Upload a text file containing your Corrosion Control Document"
    )
    
    st.subheader("Or Paste Content Directly")
    doc_text = st.text_area(
        "Paste your CCD content here:",
        height=300,
        placeholder="Paste your Corrosion Control Document content..."
    )
    
    document_content = ""
    if uploaded_file is not None:
        document_content = uploaded_file.read().decode('utf-8')
        st.success(f"✅ File uploaded: {uploaded_file.name}")
    elif doc_text.strip():
        document_content = doc_text
    
    if document_content:
        if st.button("▶️ Run Enhanced Simulation Audit", type="primary", use_container_width=True):
            st.session_state['document'] = document_content
            st.session_state['run_simulation'] = True
            st.rerun()
    else:
        st.info("👆 Please upload a file or paste document content to continue")

# Run Simulation and Show Results
if st.session_state.get('run_simulation', False):
    st.divider()
    st.header("📊 Enhanced Simulation Results")
    
    document = st.session_state.get('document', '')
    use_ml = st.session_state.get('use_ml', True)
    offline_mode = st.session_state.get('offline_mode', True)
    use_local_llm = st.session_state.get('use_local_llm', False)
    pipeline_length = st.session_state.get('pipeline_length', 1000)
    surface_area = st.session_state.get('surface_area', 1000)
    
    with st.spinner("🔄 Processing with Hybrid Physics-ML Engine..."):
        # Extract parameters
        params = DocumentProcessor.extract_parameters(document, offline_mode, use_local_llm)
        
        # Calculate corrosion with ML enhancement
        results = CorrosionEngine.calculate_corrosion(params, use_ml)
        
        # Generate report with financial analysis
        report = ReportGenerator.generate_report(params, results)
        
        # Calculate financial metrics
        try:
            from financial_analyzer import FinancialAnalyzer
            financial_available = True
        except:
            financial_available = False
    
    # ML Enhancement Badge
    if results.get('method') == 'hybrid_physics_ml':
        st.success(f"✨ ML-Enhanced Prediction (Confidence: {results['ml_confidence']*100:.1f}%)")
    
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
    
    # Financial Impact (if available)
    if financial_available and report.get('financial_summary'):
        fin = report['financial_summary']
        st.markdown(f"""
        <div class='financial-box'>
            <h3 style='color: white; margin-top: 0;'>💰 Financial Impact Assessment</h3>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; color: white;'>
                <div>
                    <div style='font-size: 14px; opacity: 0.8;'>Total Cost of Failure</div>
                    <div style='font-size: 24px; font-weight: bold;'>${fin['cof']['total_cof']/1e6:.2f}M</div>
                </div>
                <div>
                    <div style='font-size: 14px; opacity: 0.8;'>Probability of Failure</div>
                    <div style='font-size: 24px; font-weight: bold;'>{fin['probability_of_failure']*100:.1f}%</div>
                </div>
                <div>
                    <div style='font-size: 14px; opacity: 0.8;'>Expected Monetary Value</div>
                    <div style='font-size: 24px; font-weight: bold;'>${fin['expected_monetary_value']/1e6:.2f}M</div>
                </div>
            </div>
            <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.3); color: white;'>
                <strong>Financial Severity:</strong> {fin['severity']} | 
                <strong>Downtime:</strong> {fin['cof']['downtime_days']} days @ ${fin['cof']['downtime_cost']/fin['cof']['downtime_days']:,.0f}/day
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Metrics
    st.subheader("📈 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Design Life", f"{params['design_life']} years")
    
    with col2:
        delta_years = results['time_to_failure'] - params['design_life']
        st.metric(
            "Predicted Life", 
            f"{results['time_to_failure']:.1f} years",
            delta=f"{delta_years:.1f} years"
        )
    
    with col3:
        st.metric("Corrosion Rate", f"{results['corrosion_rate']:.3f} mm/yr")
    
    with col4:
        safety_margin = ((results['time_to_failure']/params['design_life'] - 1) * 100)
        st.metric("Safety Margin", f"{safety_margin:.1f}%")
    
    # ML vs Physics comparison
    if results.get('physics_rate'):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Physics-Only Rate", f"{results['physics_rate']:.3f} mm/yr")
        with col2:
            ml_adjustment = (results['corrosion_rate']/results['physics_rate'] - 1) * 100
            st.metric("ML Adjustment", f"{ml_adjustment:+.1f}%")
    
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"🟡 Design Life: {params['design_life']} years")
    with col2:
        st.error(f"🔴 Min Thickness: {params['min_thickness']} mm")
    with col3:
        st.warning(f"⚠️ Predicted Failure: {results['time_to_failure']:.1f} years")
    
    st.divider()
    
    # Recommendations with Financial ROI
    st.subheader("💡 Engineering Recommendations with Financial Analysis")
    
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
            st.markdown(f"**Technical Impact:** {rec['impact']}")
            if 'financial' in rec:
                st.markdown(f"**💰 Financial Impact:** {rec['financial']}")
    
    st.divider()
    
    # Download Report
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        report_text = ReportGenerator.generate_text_report(params, results, report)
        st.download_button(
            label="📥 Download Full Report",
            data=report_text,
            file_name=f"ccd_audit_report_{report['risk_level']}.txt",
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
