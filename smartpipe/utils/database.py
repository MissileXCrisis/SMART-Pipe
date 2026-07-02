# smartpipe/utils/database.py
import os
import urllib.request
from pathlib import Path

# Updated with hyper-stable, ultra-lightweight test data links from GitHub
MOCK_REFS = {
    "Escherichia_coli": "https://raw.githubusercontent.com/wheretrue/fasql/main/test/sql/test.fasta",
    "Staphylococcus_aureus": "https://raw.githubusercontent.com/RobersonLab/motif_scraper/master/sample_data/KI270394.fa"
}

def setup_database(db_dir):
    """
    Automates the infrastructure preparation: creates directories, downloads
    reference FASTA files, and prepares them for k-mer indexing.
    """
    db_path = Path(db_dir)
    raw_dir = db_path / "raw_references"
    index_dir = db_path / "kmer_index"
    
    # Create directory boundaries securely
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(index_dir, exist_ok=True)
    
    print(f"[DB-MANAGER] Initializing database curation workspace at: {db_path}")
    downloaded_files = []

    # Automated Download Loop
    for organism, url in MOCK_REFS.items():
        destination = raw_dir / f"{organism}.fasta"
        downloaded_files.append(destination)
        
        if destination.exists():
            print(f" -> {organism} reference already exists. Skipping download.")
            continue
            
        print(f" -> Downloading reference genome for {organism}...")
        try:
            # Safely fetch the remote file
            urllib.request.urlretrieve(url, destination)
            print(f"    ✅ Successfully saved to {destination.name}")
        except Exception as e:
            print(f"    ❌ Failed to download {organism}: {str(e)}")
            return False, []
            
    print(f"[DB-MANAGER] All {len(downloaded_files)} source genomes secured.")
    print(f"[DB-MANAGER] Workspace prepped for k-mer intersection build.")
    
    return True, downloaded_files