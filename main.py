import os
from dotenv import load_dotenv
from smartpipe.cli import parse_arguments
from smartpipe.utils.system import audit_environment

def main():
    # Load environment variables from .env file securely
    load_dotenv()
    
    # Parse CLI Arguments
    args = parse_arguments()
    
    print("🚀 Initializing SMART-Pipe...")
    print("---------------------------------------------")
    
    # Run Smart Architecture Discovery
    sys_info = audit_environment()
    
    # Determine thread execution strategy
    if args.threads:
        final_threads = args.threads
        print(f"[CONFIG] User explicitly requested {final_threads} threads.")
    else:
        final_threads = sys_info["allocated_cpus"]
        env_type = "HPC (SLURM)" if sys_info["is_hpc"] else "Local Workstation"
        print(f"[AUTO-DETECT] Environment: {env_type}. Mapping execution to {final_threads} worker thread(s).")
        
    # Verify Security Compliance
    if sys_info["has_api_key"]:
        print("[SECURITY] Gemini API Key verified in environment variables.")
    else:
        print("[WARNING] GEMINI_API_KEY not found. Automated reporting features will be disabled in Phase 4.")
        
    print("---------------------------------------------")
    print(f"Ready to process data from: {args.input}")
    print(f"Results will be routed to : {args.output}")

if __name__ == "__main__":
    main()