# 🧬 SMART-Pipe: Shotgun Metagenomic Profiling & Automated Reporting Pipeline

SMART-Pipe is an end-to-end, high-performance molecular bioinformatics pipeline built to ingest raw environmental or clinical shotgun metagenomic sequencing reads, execute parallelized quality control, perform taxonomic reference database intersection, calculate ecological diversity metrics, and programmatically generate guardrailed, natural language narrative summaries using Google GenAI.

---

## 🚀 Core Architectural Features

* **Phase 1: Environment Auto-Discovery:** Dynamic runtime detection of operating environments (Local Workstations vs. SLURM Shared HPC Nodes) to automatically scale CPU core worker limits.
* **Phase 2: Asynchronous QC & Profiling Engine:** Multiprocessing pool execution wrapping industry-standard byte-filtering utilities (`fastp`) to dynamically discover, pair (`_R1`/`_R2`), and clean paired-end FASTQ samples concurrently.
* **Phase 3: HPC Cluster Native Layer:** A decoupled, infrastructure-isolated SLURM batch submission blueprint (`sbatch`) featuring strict walltime and memory bounds to prevent thread oversubscription on multi-user nodes.
* **Phase 4: Ecological Biostatistics & Guardrailed AI Synthesis:** Integrated Python math arrays computing Alpha Diversity (Shannon Index), Beta Diversity Matrices (Bray-Curtis Dissimilarity), and a programmatic post-processing grounding guardrail layer that validates Gemini-3.5-Flash outputs against raw numerical source arrays.
* **Phase 5: Streamlit Interactive Analytics Portal:** A wide-layout analytical web application projecting interactive species relative abundance stacked charts, raw data frames, and automated narrative reports side-by-side.

---

## 📁 Repository Directory Structure

```text
smart-pipe/
├── cluster/
│   └── submit_pipeline.sh        # 📜 SLURM cluster submission template
├── databases/
│   ├── kmer_index/              # 📁 Compressed lookup matrices
│   └── raw_references/          # 📁 Curated reference genomes (.fasta)
├── logs/                        # 📁 HPC standard output & error streams
├── outputs/
│   ├── abundance/               # 📊 Individual sample abundance profiles (.tsv)
│   ├── biostatistics/           # 📉 Consolidated diversity arrays (.csv)
│   ├── reports/                 # 📄 Grounded markdown summaries (.md)
│   └── qc/                      # 🧼 Trimmed fastq.gz reads and fastp reports
├── smartpipe/                   # 🚀 Core Source Library Modules
│   ├── __init__.py
│   ├── cli.py                   # 🔧 Central CLI argument parser
│   └── utils/
│       ├── ai_report.py         # 🔌 Outbound GenAI client & grounding engine
│       ├── biostats.py          # 📐 Shannon Diversity & Bray-Curtis matrix math
│       ├── database.py          # 🗃️ Automated reference infrastructure downloader
│       ├── profiler.py          # 🧬 Taxonomic intersection simulator
│       └── system.py            # 💻 System hardware configuration auditor
├── .env                         # 🔑 Local environment secrets configuration
├── .gitignore                   # 🚫 Data and credential exclusion patterns
├── dashboard.py                 # 🌐 Streamlit GUI web portal portal
├── main.py                      # 🏁 Core production engine entrypoint
└── README.md                    # 📖 System operational documentation

⚙️ Installation & Prerequisites1. Environment DeploymentClone this repository and instantiate an isolated Python conda environment:Bashconda create -n smartpipe python=3.10 -y
conda activate smartpipe
pip install pandas numpy streamlit google-genai python-dotenv
2. External DependenciesEnsure fastp is installed and accessible within your system execution path:Bashconda install -c bioconda fastp -y
3. API Token Cryptographic ConfigurationCreate a local .env configuration template in the project root directory and map your verified Google AI Studio API key:Code snippetGEMINI_API_KEY=AIzaSyYourRegisteredGoogleAIStudioKeyHere
🛠️ Operational Execution ProtocolsStep 1: Initialize Database Curation InfrastructureExecute the pipeline maintenance flag to download, verify, and isolate your standard reference genomes:Bashpython main.py --setup-db
Step 2: Trigger End-to-End Metagenomic ProcessingRun the unified computational engine by pointing it to a directory containing raw paired-end sequence paths:Bashpython main.py -i ./mock_input -o ./outputs
Step 3: Launch Interactive Presentation InterfaceBoot up the Streamlit engine to read output matrices and render visualizations on a secure local webserver port:Bashstreamlit run dashboard.py
Access the interface locally via http://localhost:8501 in your browser framework.Step 4: Scale Out onto Compute Clusters (HPC Implementation)For shared institutional hardware infrastructure, queue the isolated batch file directly to the SLURM scheduler:Bashsbatch cluster/submit_pipeline.sh
🛡️ Grounding Validation & Benchmarking BlueprintTo guarantee biological diagnostic safety and suppress Large Language Model stochastic hallucinations, the pipeline runs an automated Grounding Guardrail Engine prior to file writes:Structural Invariant Identity Verification: Asserts that every unique sample name processed by the computing cluster is explicitly contained in the text output.Mathematical Score Reflection: Matches the floating-point values computed via the Shannon-Wiener algorithm against substrings in the report text to block semantic discrepancies.🧪 Gold-Standard Verification (The Zymo Benchmark)Production accuracy validation utilizes raw datasets derived from the public ZymoBIOMICS Microbial Community Standard (containing 8 bacteria and 2 yeasts at precise theoretical ratios). The pipeline's automated benchmarking framework validates accuracy metrics via Python data science engines:Calculates Root Mean Squared Error (RMSE) and the Coefficient of Determination ($R^2$) against manufacturer ground-truths.Enforces an embedded pipeline gatekeeper boundary condition requiring $R^2 > 0.95$ for clinical validation passes.Developed as a modular, container-ready architecture for advanced ecological metagenomic exploration.