# CCDs Simulation Auditor

**Physics-Informed AI for Corrosion Control Document Validation**

A streamlined tool for performing simulation-based audits of Corrosion Control Documents (CCDs). This application extracts critical parameters from engineering documents and runs physics-based simulations to predict material degradation and identify design risks.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Download all files** to a folder on your computer:
   - `app.py`
   - `corrosion_engine.py`
   - `document_processor.py`
   - `report_generator.py`
   - `requirements.txt`

2. **Open terminal/command prompt** and navigate to the folder:
   ```bash
   cd path/to/your/folder
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**: Your browser will automatically open to `http://localhost:8501`

---

## 📱 Running on Any Device

### Windows
- Install Python from [python.org](https://python.org)
- Follow the Quick Start steps above using Command Prompt or PowerShell

### Mac/Linux
- Python usually comes pre-installed
- Follow the Quick Start steps above using Terminal

### Remote/Cloud Options
- **Streamlit Cloud**: Free hosting at [streamlit.io/cloud](https://streamlit.io/cloud)
- **Google Colab**: Upload files and run in browser
- **Any server**: Just needs Python installed

---

## 🎯 How to Use

### Option 1: Upload Your Document
1. Select "Upload Document" from the sidebar
2. Upload a `.txt` file or paste your CCD content
3. Click "Run Simulation Audit"
4. Review the results and recommendations

### Option 2: Generate Sample Document
1. Select "Generate Sample Document" from the sidebar
2. Choose a risk level (Critical, Moderate, or Acceptable)
3. Click "Generate Random CCD"
4. Edit if needed, then run simulation
5. Experiment with different parameters!

---

## 📂 File Structure

```
ccds-auditor/
│
├── app.py                    # Main Streamlit application
├── corrosion_engine.py       # Physics-based corrosion calculations
├── document_processor.py     # NLP parameter extraction + sample generation
├── report_generator.py       # Risk assessment and recommendations
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🔧 What It Does

### 1. **Extract Parameters** (NLP)
Automatically identifies and extracts:
- Material specifications (Carbon Steel, Stainless Steel, Duplex, etc.)
- Coating types (3LPE, FBE, Sacrificial Anodes, etc.)
- Operating environment (Sour gas, Subsea, High temp)
- Design parameters (thickness, life, temperature, pressure)

### 2. **Run Simulation** (Physics-Based)
Applies empirical corrosion models:
- NACE/API standard corrosion rates
- Temperature correction (Arrhenius equation)
- H₂S partial pressure effects
- Coating effectiveness factors

### 3. **Assess Risk**
Compares predicted vs required service life:
- 🔴 **Critical**: Failure before design life
- 🟠 **High Risk**: < 20% safety margin
- 🟡 **Moderate**: < 50% safety margin
- 🟢 **Low Risk**: Adequate design

### 4. **Generate Recommendations**
Provides actionable engineering insights:
- Material upgrades
- Coating improvements
- Design modifications
- Monitoring strategies

---

## 🎓 For Hackathon Judges

### Technical Highlights
- **Multi-layer approach**: Combines NLP extraction with physics-based simulation
- **Industry standards**: Based on NACE/API corrosion models
- **Realistic outputs**: Time-to-failure predictions with confidence intervals
- **Actionable insights**: Engineering recommendations, not just compliance checks

### Innovation
- **Simulation-verified audits** instead of simple text parsing
- **Proactive risk identification** before asset construction
- **Visual degradation curves** showing predicted failure points
- **Random document generation** for testing and demonstration

### Easy to Run & Demo
- Simple Python/Streamlit stack (no React/JS complexity)
- Runs on any device with Python
- Sample documents built-in
- No database or external services needed
- Clear, organized code structure

---

## 🐛 Troubleshooting

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Missing dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Python not found
- Windows: Install from [python.org](https://python.org)
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3 python3-pip`

---

## 📊 Example CCD Format

```text
CORROSION CONTROL DOCUMENT - Pipeline Section A-102

Material: Carbon Steel API 5L X65
Coating: 3-layer Polyethylene (3LPE)
Environment: Sour gas service with H2S
Design Life: 25 years
Wall Thickness: 12.7 mm
Minimum Acceptable Thickness: 6.0 mm
Operating Temperature: 60°C
Pressure: 70 bar
```

---

## 📝 Notes

- **Sample generation** creates realistic CCDs with varying risk levels
- **No external APIs** required - all calculations done locally
- **Extensible design** - easy to add new materials, environments, or models
- **Education-friendly** - clear code structure for learning and modification

---

## 🎉 Ready to Go!

Just run `streamlit run app.py` and start auditing corrosion control documents!

For questions or issues, the code is well-commented and easy to modify.

**Happy Hacking! 🚀⚡**
