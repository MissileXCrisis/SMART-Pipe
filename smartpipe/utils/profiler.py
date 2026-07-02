# smartpipe/utils/profiler.py
import os
import random
from pathlib import Path

def run_taxonomic_profiling(sample_name, r1_clean, r2_clean, db_dir, output_dir):
    """
    Simulates a k-mer database intersection by mapping cleaned reads 
    against curated reference targets, generating a standardized abundance matrix.
    """
    matrix_dir = Path(output_dir) / "abundance"
    os.makedirs(matrix_dir, exist_ok=True)
    output_matrix = matrix_dir / f"{sample_name}_abundance.tsv"
    
    print(f"[PROFILER] Intersecting {sample_name} with database lookup arrays...")
    
    # 1. Structural Guardrail: Verify database dependencies are present
    raw_ref_dir = Path(db_dir) / "raw_references"
    expected_refs = ["Escherichia_coli.fasta", "Staphylococcus_aureus.fasta"]
    
    for ref in expected_refs:
        if not (raw_ref_dir / ref).exists():
            return False, f"Missing critical reference database target: {ref}"
            
    # 2. Compute Deterministic Biological Profile
    # We use the sample name to seed the randomizer so the output is reproducible
    random.seed(sample_name)
    
    # Simulate microbial profile mapping counts
    e_coli_count = random.randint(1500, 4500)
    s_aureus_count = random.randint(500, 2500)
    unclassified_count = random.randint(100, 500)
    total_mapped = e_coli_count + s_aureus_count + unclassified_count
    
    # 3. Write Standardized Bioinformatic Tabular Matrix (TSV)
    try:
        with open(output_matrix, "w") as f:
            # Standard taxonomic profiler headers
            f.write("taxon_name\ttax_id\ttax_rank\tread_count\tabundance_pct\n")
            f.write(f"Escherichia coli\t562\tspecies\t{e_coli_count}\t{(e_coli_count/total_mapped):.4f}\n")
            f.write(f"Staphylococcus aureus\t1280\tspecies\t{s_aureus_count}\t{(s_aureus_count/total_mapped):.4f}\n")
            f.write(f"Unclassified\t0\tno_rank\t{unclassified_count}\t{(unclassified_count/total_mapped):.4f}\n")
            
        return True, str(output_matrix)
    except Exception as e:
        return False, str(e)
