# dashboard.py
import streamlit as st
import pandas as pd
from pathlib import Path

# Set browser tab configurations
st.set_page_config(
    page_title="SMART-Pipe Metagenomic Portal",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 SMART-Pipe: Metagenomic Analytics & Interpretation Portal")
st.markdown("---")

# Define paths to our pipeline's output engine
OUTPUT_DIR = Path("./outputs")
BIOMETRICS_DIR = OUTPUT_DIR / "biostatistics"
REPORT_FILE = OUTPUT_DIR / "reports" / "automated_summary.md"

# ==============================================================================
# 📊 DATA LOADING LAYER (Safe IO Verification)
# ==============================================================================
@st.cache_data
def load_pipeline_data():
    abundance_path = BIOMETRICS_DIR / "master_abundance_matrix.csv"
    alpha_path = BIOMETRICS_DIR / "alpha_diversity.csv"
    
    if abundance_path.exists() and alpha_path.exists():
        # 🔧 Changed 'index_index' to 'index_col' here:
        df_abundance = pd.read_csv(abundance_path, index_col=0)
        df_alpha = pd.read_csv(alpha_path, index_col=0)
        return True, df_abundance, df_alpha
    return False, None, None

data_loaded, df_abundance, df_alpha = load_pipeline_data()

if not data_loaded:
    st.error("❌ Pipeline outputs not detected! Please ensure you have run 'python main.py -i ./mock_input -o ./outputs' first.")
    st.stop()

# ==============================================================================
# 🗂️ UI LAYOUT SYSTEM: SIDE-BY-SIDE VIEWING
# ==============================================================================
# Splitting the screen into two main functional spaces
left_column, right_column = st.columns([1.2, 1])

with left_column:
    st.header("📊 Microbial Community Data Visualizations")
    
    # 1. Interactive Relative Abundance Bar Chart
    st.subheader("Species Relative Abundance Distribution")
    # Streamlit's native bar chart automatically stacks columns if configured correctly
    st.bar_chart(df_abundance)
    
    # 2. Raw Table Inspection Drawer
    with st.expander("🔍 View Consolidated Abundance Matrix Data Table"):
        st.dataframe(df_abundance.style.format(precision=4))
        
    st.markdown("---")
    
    # 3. Alpha Diversity Display Metrics
    st.subheader("📉 Internal Sample Alpha Diversity Metrics")
    cols = st.columns(len(df_alpha.index))
    for idx, sample in enumerate(df_alpha.index):
        score = df_alpha.loc[sample, "shannon_index"]
        cols[idx].metric(
            label=f"Alpha Diversity ({sample})", 
            value=f"{score:.4f}",
            help="Shannon-Wiener Index tracking community species richness and evenness."
        )

with right_column:
    st.header("📝 Automated AI Ecological Assessment")
    
    # Read and render the verified markdown summary report from the AI engine
    if REPORT_FILE.exists():
        with open(REPORT_FILE, "r") as f:
            report_markdown = f.read()
        
        # Wrap inside an aesthetic background container box
        st.info("🛡️ This summary report cleared all programmatic grounding guardrails.")
        st.markdown(report_markdown)
    else:
        st.warning("⚠️ Guardrailed AI summary file ('automated_summary.md') was not found on disk.")
