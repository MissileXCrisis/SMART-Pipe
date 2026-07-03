import os
import sys
import multiprocessing
from pathlib import Path
from dotenv import load_dotenv
from smartpipe.cli import parse_arguments
from smartpipe.utils.system import audit_environment
from smartpipe.utils.qc import discover_and_pair_samples, qc_worker_wrapper
from smartpipe.utils.database import setup_database
from smartpipe.utils.profiler import run_taxonomic_profiling
from smartpipe.utils.biostats import run_biostatistical_analysis
from smartpipe.utils.ai_report import generate_automated_report  # 👈 ADD THIS IMPORT

def main():
    load_dotenv()
    args = parse_arguments()
    
    print("🚀 Initializing SMART-Pipe Engine...")
    print("---------------------------------------------")
    
    # Handle Database Setup Task
    if args.setup_db:
        success, refs = setup_database(args.db)
        if success:
            print("---------------------------------------------")
            print("🎉 Reference database infrastructure setup complete!")
        else:
            print("❌ Reference database setup failed.")
        sys.exit(0)

    # Argument validation
    if not args.input or not args.output:
        print("❌ Error: Missing required arguments. Please provide -i and -o.")
        sys.exit(1)

    # Phase 1: Environment Discovery
    sys_info = audit_environment()
    final_threads = args.threads if args.threads else sys_info["allocated_cpus"]
        
    print(f"[SYSTEM] Mapping execution to {final_threads} max pool workers.")
    print(f"[DATABASE] Directing pipeline lookup matrix to: {args.db}")
    print("---------------------------------------------")
    
    # Phase 2: Sample Discovery
    print(f"[DISCOVERY] Scanning directory: {args.input}")
    sample_pairs = discover_and_pair_samples(args.input)
    print(f"[DISCOVERY] Found {len(sample_pairs)} complete paired-end sample(s).")
    
    if not sample_pairs:
        print("❌ Error: No valid data found. Exiting.")
        sys.exit(1)

    # Run Concurrent QC Layer
    worker_tasks = [(name, r1, r2, args.output) for name, r1, r2 in sample_pairs]
    pool_size = min(final_threads, len(sample_pairs))
    
    print(f"\n⚡ Executing Parallel Quality Control...")
    with multiprocessing.Pool(processes=pool_size) as pool:
        qc_results = pool.map(qc_worker_wrapper, worker_tasks)
        
    print("\n📊 Run Execution Summary:")
    print("---------------------------------------------")
    
    any_profiled = False
    for success, sample, message in qc_results:
        if success:
            print(f" ✅ Sample: {sample.ljust(15)} | QC: Passed")
            clean_r1 = os.path.join(args.output, f"{sample}_R1_clean.fastq.gz")
            clean_r2 = os.path.join(args.output, f"{sample}_R2_clean.fastq.gz")
            
            prof_success, prof_msg = run_taxonomic_profiling(sample, clean_r1, clean_r2, args.db, args.output)
            if prof_success:
                print(f"    └── 🧬 Taxonomic Profiling Matrix saved to: {Path(prof_msg).name}")
                any_profiled = True
            else:
                print(f"    └── ❌ Profiling Failed: {prof_msg}")
        else:
            print(f" ❌ Sample: {sample.ljust(15)} | QC: Failed ({message})")
            
    print("---------------------------------------------")
    
    # Trigger Biostatistical Synthesis
    if any_profiled:
        abundance_folder = os.path.join(args.output, "abundance")
        stats_success, stats_data = run_biostatistical_analysis(abundance_folder, args.output)
        if stats_success:
            print("🎉 Biostatistical analysis matrices calculated and stored!")
            print("---------------------------------------------")
            
            # ==============================================================================
            # 🔌 Phase 4, Step 2: Trigger Outbound AI Integration Layer
            # ==============================================================================
            ai_success, ai_payload = generate_automated_report(stats_data)
            if ai_success:
                print("✅ AI Interpretation Payload Received Successfully!")
                print("\n--- Live Preview of Gemini Summary ---")
                print(ai_payload)
                print("--------------------------------------")
            else:
                print(f"❌ AI Synthesis Failed: {ai_payload}")
        else:
            print(f"❌ Biostatistical analysis failed: {stats_data}")
    else:
        print("[WARNING] No samples successfully completed profiling. Skipping statistics.")
        
    print("🎉 Pipeline run stage finished successfully!")

if __name__ == "__main__":
    main()