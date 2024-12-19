# **SaraGMake**: Snakemake Pipeline for Subtyping *Blastocystis sp.* from ONT Raw Reads (Ubuntu)

Welcome to **SaraGMake**! This Snakemake pipeline is designed for subtyping *Blastocystis sp.* from Oxford Nanopore Technologies (ONT) raw sequencing reads.

---

## **Instructions**

Before you begin, make sure that **Bioconda** is already installed on your system.

### 1. **Install Prerequisites**

Run the `Installation_snakemake.bash` script to automatically install all the necessary prerequisites for using the Snakemake pipeline.

```bash
bash Installation_snakemake.bash

2. Prepare Your Experiment Directory

Create a directory for your experiment. For example, name it Snakemake_Blastocystis:

mkdir Snakemake_Blastocystis
cd Snakemake_Blastocystis

Inside this directory, you should organize the following subdirectories:

Snakemake_Blastocystis/
  ├── data/
  │   └── Raw/
  │       └── <Your .fastq raw data files>
  ├── results/
  ├── scripts/
  │   └── <Extract and add script files here>
  └── <Add the Snakemake workflow file here>

    data/Raw/: Place your raw .fastq data files here.
    scripts/: Extract the script .zip file and add them here.
    results/: This directory will store the output files.
    Snakemake Workflow: Place the Snakemake .smk file (your pipeline) here.

How to Run the Pipeline in the Terminal

    Navigate to the Snakemake Directory

Change to the directory where your Snakemake workflow is located:

cd /path/to/Snakemake_Blastocystis

    Run Snakemake

Simply run the following command to execute the pipeline:

snakemake --cores 4

This will execute the pipeline using 4 cores (adjust the number of cores based on your machine’s capacity).
Additional Notes

    Ensure that you have all necessary permissions and the environment set up before running the script.
    If you face any issues, feel free to open an issue on this repository for support!






 
