# smartpipe/utils/qc.py
import os
import subprocess
from pathlib import Path

def discover_and_pair_samples(input_dir):
    """
    Scans the input directory and matches paired-end files (_R1 and _R2).
    Returns a list of tuples: [(sample_name, r1_path, r2_path), ...]
    """
    paired_samples = {}
    
    # Handle paths robustly
    input_path = Path(input_dir)
    if not input_path.exists():
        return []

    # Scan for gzipped fastq files
    for file in input_path.glob("*.fastq.gz"):
        filename = file.name
        # Extract base sample name before the first underscore
        sample_name = filename.split('_')[0]
        
        if sample_name not in paired_samples:
            paired_samples[sample_name] = {"R1": None, "R2": None}
            
        if "_R1" in filename:
            paired_samples[sample_name]["R1"] = str(file)
        elif "_R2" in filename:
            paired_samples[sample_name]["R2"] = str(file)

    # Convert dictionary to clean list of validated pairs
    final_pairs = []
    for name, reads in paired_samples.items():
        if reads["R1"] and reads["R2"]:
            final_pairs.append((name, reads["R1"], reads["R2"]))
        else:
            print(f"[WARNING] Skipping incomplete pair for sample: {name}")
            
    return final_pairs


def qc_worker_wrapper(args_tuple):
    """
    Unpacks a single tuple argument so it can be cleanly mapped 
    across a multiprocessing pool.
    """
    sample_name, r1_path, r2_path, output_dir = args_tuple
    
    # Re-use our original processing logic
    os.makedirs(output_dir, exist_ok=True)
    out_f = os.path.join(output_dir, f"{sample_name}_R1_clean.fastq.gz")
    out_r = os.path.join(output_dir, f"{sample_name}_R2_clean.fastq.gz")
    html_report = os.path.join(output_dir, f"{sample_name}_fastp.html")
    json_report = os.path.join(output_dir, f"{sample_name}_fastp.json")
    
    cmd = [
        "fastp", "-i", r1_path, "-I", r2_path,
        "-o", out_f, "-O", out_r,
        "-h", html_report, "-j", json_report,
        "--detect_adapter_for_pe"
    ]
    
    try:
        # Run silently inside the worker process; don't bloat the main terminal
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True, sample_name, "Success"
    except Exception as e:
        return False, sample_name, str(e)