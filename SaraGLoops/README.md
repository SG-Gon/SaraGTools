# ✨ SaraGLoops ✨

SaraGLoops is a tool designed to process Oxford Nanopore Technologies (ONT) raw sequencing reads. This tool is adapted for existing programs and allows you to handle numerous sequences at once 🧬🔬

## 📝 Instructions 📜
Before you get started, ensure that Bioconda is installed on your system 🛠️

### 1️⃣ Install Prerequisites ⚙️

Before running the pipeline, make sure to install all the necessary dependencies by running the provided script:

bash Installation_snakemake.bash

This will automatically install Snakemake and other required tools.
### 2️⃣ Running the SaraGLoops Scripts 🎬

All the scripts in SaraGLoops are self-explanatory and should work out of the box. However, there’s an exception for SaraSID, which requires creating a custom database from a FASTA file.

### ⚠️ Exceptions for SaraSID ⚠️

SaraSID is a tool that requires a custom database for subtyping. Please follow these steps to create the necessary database:
Steps to Create a Custom Database 📚

    Create a Directory for SaraSID 📂 Create a new directory for SaraSID and navigate into it.


Prepare Your FASTA File 📑 You will need a FASTA file that contains the reference sequences (e.g., ref_library).

Create the Database 🛠️ Use the makeblastdb command to create a BLAST database from your FASTA file.

Run the following command:

makeblastdb -in ref_library -parse_seqids -out ref_library -dbtype nucl

    -in: Input your FASTA file.
    -out: This will specify the output database name.
    -dbtype nucl: This indicates the type of the database (for nucleotide sequences).

Ensure SaraSID and Database Are in the Same Directory 💾

Once the database is created, make sure the SaraSID script and the database are in the same directory.

Run the SaraSID Script 🚀

After setting up the database, run the SaraSID script:

python /path/to/SaraSID.py

Follow the on-screen instructions to continue with the subtyping process.
