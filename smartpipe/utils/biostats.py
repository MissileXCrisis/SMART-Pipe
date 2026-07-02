# smartpipe/utils/biostats.py
import os
import numpy as np
import pandas as pd
from pathlib import Path

def calculate_shannon_index(abundance_array):
    """
    Calculates the Shannon-Wiener Diversity Index (H') for a 1D array of proportions.
    H' = -sum(p_i * ln(p_i))
    """
    # Filter out zeros to avoid log(0) errors
    p = abundance_array[abundance_array > 0]
    return -np.sum(p * np.log(p))

def calculate_bray_curtis(sample_a, sample_b):
    """
    Calculates the Bray-Curtis Dissimilarity between two abundance arrays.
    BC = 1 - (2 * sum(min(a_i, b_i)) / sum(a_i + b_i))
    """
    min_sum = np.sum(np.minimum(sample_a, sample_b))
    total_sum = np.sum(sample_a + sample_b)
    if total_sum == 0:
        return 0.0
    return 1.0 - (2.0 * min_sum / total_sum)

def run_biostatistical_analysis(abundance_dir, output_dir):
    """
    Consolidates individual sample TSVs into a master matrix and computes
    ecological metrics (Alpha & Beta Diversity).
    """
    abundance_path = Path(abundance_dir)
    if not abundance_path.exists():
        return False, "Abundance directory does not exist."
        
    tsv_files = list(abundance_path.glob("*_abundance.tsv"))
    if not tsv_files:
        return False, "No taxonomy abundance matrices found to analyze."

    print(f"[BIOSTATS] Compiling master ecological matrix from {len(tsv_files)} samples...")
    
    # 1. Parse and build a consolidated DataFrame
    master_data = {}
    for file in tsv_files:
        sample_name = file.name.split('_')[0]
        df = pd.read_csv(file, sep="\t")
        # Ensure we map taxon_name to its abundance percentage
        master_data[sample_name] = df.set_index("taxon_name")["abundance_pct"].to_dict()
        
    master_df = pd.DataFrame(master_data).fillna(0.0).T
    # Columns are taxa (E. coli, S. aureus, Unclassified), Rows are samples (SampleA, B, C)

    # 2. Compute Alpha Diversity (Shannon Index)
    print("[BIOSTATS] Calculating Alpha Diversity (Within-Sample Evenness)...")
    alpha_results = {}
    for sample in master_df.index:
        alpha_results[sample] = calculate_shannon_index(master_df.loc[sample].values)
        
    # 3. Compute Beta Diversity Matrix (Bray-Curtis Dissimilarity)
    print("[BIOSTATS] Calculating Beta Diversity Matrix (Between-Sample Distance)...")
    samples = list(master_df.index)
    beta_matrix = pd.DataFrame(0.0, index=samples, columns=samples)
    
    for i in range(len(samples)):
        for j in range(i, len(samples)):
            s1 = samples[i]
            s2 = samples[j]
            bc_value = calculate_bray_curtis(master_df.loc[s1].values, master_df.loc[s2].values)
            beta_matrix.loc[s1, s2] = bc_value
            beta_matrix.loc[s2, s1] = bc_value  # Symmetric matrix

    # 4. Save results securely to the output directory
    stats_output_dir = Path(output_dir) / "biostatistics"
    os.makedirs(stats_output_dir, exist_ok=True)
    
    alpha_df = pd.DataFrame.from_dict(alpha_results, orient="index", columns=["shannon_index"])
    alpha_df.to_csv(stats_output_dir / "alpha_diversity.csv")
    beta_matrix.to_csv(stats_output_dir / "beta_diversity_bray_curtis.csv")
    master_df.to_csv(stats_output_dir / "master_abundance_matrix.csv")
    
    print(f"[BIOSTATS] Ecology arrays successfully written to: {stats_output_dir}")
    return True, {
        "master_matrix": master_df.to_dict(orient="index"),
        "alpha": alpha_results,
        "beta": beta_matrix.to_dict(orient="index")
    }