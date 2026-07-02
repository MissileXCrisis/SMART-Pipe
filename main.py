import os
import sys
import multiprocessing
from dotenv import load_dotenv
from smartpipe.cli import parse_arguments
from smartpipe.utils.system import audit_environment
from smartpipe.utils.qc import discover_and_pair_samples, qc_worker_wrapper
from smartpipe.utils.database import setup_database

def main():
    load_dotenv()
    args = parse_arguments()
    
    print("🚀 Initializing SMART-Pipe Engine...")
    print("---------------------------------------------")
    
    # 1. Handle Isolated Database Setup Utility first if requested
    if args.setup_db:
        success, refs = setup_database(args.db)
        if success:
            print("---------------------------------------------")
            print("🎉 Reference database infrastructure setup complete!")
        else:
            print("❌ Reference database setup failed.")
        sys.exit(0) # Exit cleanly after running maintenance task

    # 2. Fall back to standard Sample Processing pipeline if --setup-db wasn't called
    if not args.input or not args.output:
        print("❌ Error: Missing required arguments for processing. Please provide -i/--input and -o/--output.")
        print("💡 Hint: Run with --setup-db to download references first, or use -h for help.")
        sys.exit(1)

    # Phase 1: Environment Discovery
    sys_info = audit_environment()
    final_threads = args.threads if args.threads else sys_info["allocated_cpus"]
        
    print(f"[SYSTEM] Mapping execution to {final_threads} max pool workers.")
    print(f"[DATABASE] Directing pipeline lookup matrix to: {args.db}")
    print("---------------------------------------------")
    
    # Phase 2: Sample Processing
    print(f"[DISCOVERY] Scanning directory: {args.input}")
    sample_pairs = discover_and_pair_samples(args.input)
    print(f"[DISCOVERY] Found {len(sample_pairs)} complete paired-end sample(s).")
    
    if not sample_pairs:
        print("❌ Error: No valid data found. Exiting.")
        sys.exit(1)

    worker_tasks = [(name, r1, r2, args.output) for name, r1, r2 in sample_pairs]
    pool_size = min(final_threads, len(sample_pairs))
    
    with multiprocessing.Pool(processes=pool_size) as pool:
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