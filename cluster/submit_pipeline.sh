#!/bin/bash

# ==============================================================================
# 📜 SLURM Resource Allocation Boundaries (Phase 3, Steps 1 & 2)
# ==============================================================================
#SBATCH --job-name=SMART-Pipe          # Human-readable name of the job in the queue
#SBATCH --output=logs/sp_run_%j.log    # Direct standard output stream (%j injects unique Job ID)
#SBATCH --error=logs/sp_run_%j.err     # Direct standard error stream (%j injects unique Job ID)
#SBATCH --nodes=1                      # Request exactly 1 physical compute node
#SBATCH --ntasks=1                     # Run 1 top-level execution task (our Python main.py)
#SBATCH --cpus-per-task=8              # Request 8 physical CPU cores for our worker pool
#SBATCH --mem=32G                      # Secure 32 Gigabytes of RAM for memory isolation
#SBATCH --time=02:00:00                # Walltime constraint: Max 2 hours execution window
#SBATCH --partition=standard           # Target cluster queue partition (e.g., standard, batch)

# Exit immediately if any individual command fails
set -e

echo "🚀 SLURM Job ID: $SLURM_JOB_ID initialized on node: $SLURMD_NODENAME"
echo "📅 Execution Started: $(date)"
echo "--------------------------------------------------------"

# ==============================================================================
# 🔧 Environment Initialization
# ==============================================================================
# Adjust this to point to your cluster's miniconda/anaconda base installation path
# Typically found at /home/username/miniconda3/etc/profile.d/conda.sh on an HPC cluster
CONDA_PROFILE_PATH="$HOME/anaconda3/etc/profile.d/conda.sh"

if [ -f "$CONDA_PROFILE_PATH" ]; then
    source "$CONDA_PROFILE_PATH"
    conda activate smartpipe
    echo "[HPC-ENV] Successfully loaded and activated 'smartpipe' conda environment."
else
    echo "❌ Error: Conda profile initialization script not found at $CONDA_PROFILE_PATH"
    exit 1
fi

# Navigate to the root project directory relative to this script's location
cd "$(dirname "$0")/.."

# ==============================================================================
# 🗺️ Pipeline Configuration Envelopes
# ==============================================================================
# Encapsulating paths without touching the core Python source code
INPUT_DIR="./mock_input"
OUTPUT_DIR="./outputs"
DB_DIR="./databases"

echo "[CONFIG] Input target:  $INPUT_DIR"
echo "[CONFIG] Output target: $OUTPUT_DIR"
echo "[CONFIG] Database path: $DB_DIR"
echo "[SYSTEM] Cluster allocated threads: $SLURM_CPUS_PER_TASK"
echo "--------------------------------------------------------"

# ==============================================================================
# ⚡ Pipeline Execution
# ==============================================================================
# Note: We intentionally omit the "-t/--threads" flag here. 
# SMART-Pipe will automatically discover $SLURM_CPUS_PER_TASK via Phase 1 code!
python main.py \
    --input "$INPUT_DIR" \
    --output "$OUTPUT_DIR" \
    --db "$DB_DIR"

echo "--------------------------------------------------------"
echo "🎉 Job Finished: $(date)"