import argparse
from smartpipe.utils.system import audit_environment

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="SMART-Pipe: Shotgun Metagenomic Profiling and Automated Reporting Pipeline"
    )
    
    parser.add_init = parser.add_argument_group("Required Arguments")
    parser.add_argument("-i", "--input", required=True, help="Directory containing raw fastq/fastq.gz sequencing reads")
    parser.add_argument("-o", "--output", required=True, help="Directory to save pipeline outputs and report")
    
    parser.add_argument(
        "-t", "--threads", 
        type=int, 
        default=None, 
        help="Max threads to utilize. If omitted, SMART-Pipe will auto-discover available resources."
    )
    
    return parser.parse_args()