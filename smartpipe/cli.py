# smartpipe/cli.py
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="SMART-Pipe: Shotgun Metagenomic Profiling and Automated Reporting Pipeline"
    )
    
    # Execution targets
    parser.add_argument("-i", "--input", help="Directory containing raw fastq/fastq.gz sequencing reads")
    parser.add_argument("-o", "--output", help="Directory to save pipeline outputs and report")
    
    # Database configurations
    parser.add_argument(
        "-d", "--db", 
        default="./databases", 
        help="Directory to store/look for the curated reference database (Default: ./databases)"
    )
    parser.add_argument(
        "--setup-db", 
        action="store_true", 
        help="Trigger the automated download and formatting routine for reference databases"
    )
    
    parser.add_argument(
        "-t", "--threads", 
        type=int, 
        default=None, 
        help="Max threads to utilize."
    )
    
    return parser.parse_args()