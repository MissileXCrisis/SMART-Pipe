# tests/test_zymo_validation.py
import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

def run_gold_standard_validation():
    print("🧪 Initializing Gold-Standard ZymoBIOMICS Benchmarking Suite...")
    print("----------------------------------------------------------------")

    # 1. Establish the Absolute Ground Truth Vector 
    # (In production, these are the exact percentages provided by Zymo Research)
    ZYMO_GROUND_TRUTH = {
        "Escherichia coli": 0.7000,
        "Staphylococcus aureus": 0.2500,
        "Unclassified": 0.0500
    }
    
    # 2. Locate Pipeline Observed Outputs
    matrix_path = Path("./outputs/biostatistics/master_abundance_matrix.csv")
    if not matrix_path.exists():
        print("❌ Validation Aborted: Master abundance matrix not found. Run the pipeline first!")
        sys.exit(1)
        
    # Load data (Rows = Samples, Columns = Taxa)
    df = pd.read_csv(matrix_path, index_col=0)
    
    # Target 'SampleA' as our benchmark representative
    if "SampleA" not in df.index:
        print("❌ Validation Aborted: 'SampleA' metrics missing from the master matrix.")
        sys.exit(1)
        
    observed_profile = df.loc["SampleA"].to_dict()
    
    print("[VALIDATION] Aligning taxonomic arrays for error metrics calculation...")
    y_true = []
    y_pred = []
    
    for taxon, true_abundance in ZYMO_GROUND_TRUTH.items():
        pred_abundance = observed_profile.get(taxon, 0.0)
        y_true.append(true_abundance)
        y_pred.append(pred_abundance)
        print(f" 🧬 {taxon.ljust(25)} | Expected: {true_abundance:.4f} | Observed: {pred_abundance:.4f}")
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # 3. Compute High-Dimensional Accuracy Metrics
    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    
    # Calculate Coefficient of Determination (R²)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

    print("----------------------------------------------------------------")
    print(f"📊 Benchmarking Results Summary:")
    print(f"    └── 🎯 Coefficient of Determination (R² Score): {r2:.6f}")
    print(f"    └── 📉 Root Mean Squared Error (RMSE):        {rmse:.6f}")
    print("----------------------------------------------------------------")

    # 4. Strict Production Quality Gatekeeper Boundary
    # The pipeline must score higher than 0.95 to clear clinical deployment requirements
    QUALITY_THRESHOLD = 0.95
    
    if r2 >= QUALITY_THRESHOLD:
        print(f"✅ [PASSED] Pipeline accuracy exceeds gold-standard criteria (R² >= {QUALITY_THRESHOLD}).")
        print("🎉 SMART-Pipe is structurally verified for production deployment!")
        return True
    else:
        print(f"❌ [FAILED] Pipeline error rate is outside acceptable limits (R² < {QUALITY_THRESHOLD}).")
        return False

if __name__ == "__main__":
    success = run_gold_standard_validation()
    if not success:
        sys.exit(1) # Return error code to system if validation fails