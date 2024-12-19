import os

# Automatically get the list of .fastq files in the data/raw directory
# If no files are found, raise an error for easier debugging
if not os.path.exists("data/raw/"):
    raise FileNotFoundError("The 'data/raw/' directory does not exist. Please create it and add your .fastq files.")
samples = [f.replace(".fastq", "") for f in os.listdir("data/raw/") if f.endswith(".fastq")]
if not samples:
    raise ValueError("No .fastq files were found in 'data/raw/'. Please add your raw FASTQ files.")

print(f"Samples detected: {samples}")

# Define the rule for the final output (to be generated)
rule all:
    input:
        expand("results/results_filtered/{sample}_filtered_blast_results.xlsx", sample=samples)

# Rule for Nanofilt - trim the raw fastq files
rule nanofilt:
    input:
        "data/raw/{sample}.fastq"  # Input FASTQ file for the sample
    output:
        "results/trimmed/{sample}_trimmed.fastq"  # Output trimmed FASTQ file
    shell:
        """
        echo "Running NanoFilt on {input} to generate {output}"
        mkdir -p results/trimmed
        NanoFilt -q10 -l 200 --maxlength 350 {input} > {output}
        """

# Rule for NanoPlot - generate the quality report for trimmed sequences
rule nanoplot:
    input:
        fastq="results/trimmed/{sample}_trimmed.fastq"  # Input trimmed FASTQ file
    output:
        directory="results/nanoplot/{sample}/nanoplot_files"  # Output directory for NanoPlot
    shell:
        """
        echo "Checking input file: {input.fastq}"
        if [ ! -f {input.fastq} ]; then
            echo "Error: Input file {input.fastq} does not exist!"
            exit 1
        fi

        echo "Creating output directory: {output.directory}"
        mkdir -p {output.directory}

        echo "Running NanoPlot for sample: {wildcards.sample}"
        NanoPlot --fastq {input.fastq} --outdir {output.directory} --title {wildcards.sample} --dpi 300 --verbose
        """

# Rule for generating centroids using SaraTroid.sh
rule generate_centroids:
    input:
        trimmed="results/trimmed/{sample}_trimmed.fastq"  # Single input file
    output:
        centroid="results/centroids/centroid_{sample}_trimmed.fasta"
    shell:
        """
        echo "Running SaraTroid.sh on {input.trimmed} to generate {output.centroid}"
        bash scripts/SaraTroid.sh {input.trimmed} $(dirname {output.centroid})
        """

# Rule for polishing
rule polishing:
    input:
        fasta="results/centroids/centroid_{sample}_trimmed.fasta"  # Input from the centroids directory
    output:
        polished="results/polished/{sample}_polished.fasta"  # Polished output file
    shell:
        """
        echo "Polishing {input.fasta} to create {output.polished}"
        mkdir -p results/polished
        python scripts/SaraPolish.py {input.fasta} {output.polished}
        """

# Rule for PARSID - run BLAST using the polished sequences
rule parsid:
    input:
        fasta="results/polished/{sample}_polished.fasta",
        ref_library="scripts/ref_library.fasta"  # Reference library path
    output:
        excel="results/parsid/{sample}_blast_results.xlsx"
    shell:
        """
        echo "Running PARSID on {input.fasta} against reference library {input.ref_library}"
        mkdir -p results/parsid
        python scripts/SaraSID.py {input.fasta} {input.ref_library} {output.excel}
        """

# Rule for filtering BLAST results
rule filter_results:
    input:
        parsid_output="results/parsid/{sample}_blast_results.xlsx"
    output:
        filtered_excel="results/results_filtered/{sample}_filtered_blast_results.xlsx"
    shell:
        """
        echo "Filtering BLAST results for {input.parsid_output} into {output.filtered_excel}"
        mkdir -p results/results_filtered
        python scripts/Sara_Result_filtering.py {input.parsid_output} {output.filtered_excel}
        """

