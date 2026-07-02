import os
import multiprocessing
from dotenv import load_dotenv
from smartpipe.cli import parse_arguments
from smartpipe.utils.system import audit_environment
from smartpipe.utils.qc import discover_and_pair_samples, qc_worker_wrapper

def main():
    load_dotenv()
    args = parse_arguments()
    
    print("🚀 Initializing SMART-Pipe Engine...")
    print("---------------------------------------------")
    
    # Phase 1: Environment Discovery
    sys_info = audit_environment()
    if args.threads:
        final_threads = args.threads
        print(f"[CONFIG] User defined processing cap: {final_threads} thread(s).")
    else:
        final_threads = sys_info["allocated_cpus"]
        env_type = "HPC (SLURM)" if sys_info["is_hpc"] else "Local Workstation"
        print(f"[AUTO-DETECT] Environment: {env_type}. Mapping to {final_threads} max pool workers.")
        
    print("---------------------------------------------")
    
    # Phase 2: Sample Discovery
    print(f"[DISCOVERY] Scanning directory: {args.input}")
    sample_pairs = discover_and_pair_samples(args.input)
    print(f"[DISCOVERY] Found {len(sample_pairs)} complete paired-end sample(s) to process.")
    
    if not sample_pairs:
        print("❌ Error: No valid paired-end sequencing reads found. Exiting.")
        return

    # Phase 2: Concurrent Task Management
    # Pack up the configuration parameters into tuples for the worker pool
    worker_tasks = [
        (sample_name, r1, r2, args.output) 
        for sample_name, r1, r2 in sample_pairs
    ]
    
    print(f"\n⚡ Spawning Multiprocessing Pool (Workers: {min(final_threads, len(sample_pairs))})...")
    
    # Initialize the parallel process context
    # Note: min() prevents spawning more workers than actual tasks available
    pool_size = min(final_threads, len(sample_pairs))
    with multiprocessing.Pool(processes=pool_size) as pool:
        # map executes the worker tasks concurrently
        results = pool.map(qc_worker_wrapper, worker_tasks)
        
    print("\n📊 Concurrent Execution Summary:")
    print("---------------------------------------------")
    for success, sample, message in results:
        status_icon = "✅" if success else "❌"
        print(f" {status_icon} Sample: {sample.ljust(15)} | Status: {message}")
    print("---------------------------------------------")
    print("🎉 Pipeline run stage finished successfully!")

if __name__ == "__main__":
    main()