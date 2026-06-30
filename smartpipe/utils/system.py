import os
import multiprocessing

def audit_environment():
    """
    Audits the host OS to detect SLURM allocations or local physical hardware constraints.
    Returns a dictionary of runtime parameters.
    """
    audit_results = {
        "is_hpc": False,
        "allocated_cpus": 1,
        "has_api_key": False
    }
    
    # 1. Check for SLURM Environment Variables
    # SLURM_CPUS_PER_TASK is set when using srun/sbatch with -c flag
    # SLURM_JOB_CPUS_PER_NODE is a fallback for raw node allocations
    slurm_cpus = os.environ.get("SLURM_CPUS_PER_TASK") or os.environ.get("SLURM_JOB_CPUS_PER_NODE")
    
    if slurm_cpus:
        audit_results["is_hpc"] = True
        # Parse potential slurm formats (e.g., "4" or "2(x2)")
        try:
            audit_results["allocated_cpus"] = int(slurm_cpus.split('(')[0])
        except ValueError:
            audit_results["allocated_cpus"] = multiprocessing.cpu_count()
    else:
        # Fallback to local physical core detection
        audit_results["allocated_cpus"] = multiprocessing.cpu_count()
        
    # 2. Check for Gemini API Key Security Guardrail
    if os.environ.get("GEMINI_API_KEY"):
        audit_results["has_api_key"] = True
        
    return audit_results