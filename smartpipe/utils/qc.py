# smartpipe/utils/qc.py
import subprocess
import os
from pathlib import Path

def run_quality_control(input_forward, input_reverse, output_dir):
    """
    Wraps an external QC utility (fastp) to trim adapters and low-quality bases.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Robustly handle different naming structures to extract sample name
    sample_name = Path(input_forward).name.split('_')[0]
    
    out_f = os.path.join(output_dir, f"{sample_name}_R1_clean.fastq.gz")
    out_r = os.path.join(output_dir, f"{sample_name}_R2_clean.fastq.gz")
    html_report = os.path.join(output_dir, f"{sample_name}_fastp.html")
    json_report = os.path.join(output_dir, f"{sample_name}_fastp.json")
    
    cmd = [
        "fastp",
        "-i", str(input_forward),
        "-I", str(input_reverse),
        "-o", out_f,
        "-O", out_r,
        "-h", html_report,
        "-j", json_report,
        "--detect_adapter_for_pe"
    ]
    
    try:
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            check=True
        )
        return True, f"Successfully processed {sample_name}"
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        error_msg = getattr(e, 'stderr', 'Executable missing')
        return False, f"Failed processing {sample_name}: {error_msg}"
