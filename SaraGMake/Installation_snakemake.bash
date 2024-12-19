#!/bin/bash

# Welcome message
echo "Installing bioinformatics tools in the active Conda environment..."

# Check if Conda environment is active
if [ -z "$CONDA_PREFIX" ]; then
    echo "Error: No Conda environment is active. Please activate your environment and rerun this script."
    exit 1
fi

# Install Python-based tools via Conda to avoid conflicts
echo "Installing Python-based tools: NanoFilt, NanoPlot, and others..."
conda install -c bioconda nanofilt nanoplot vsearch pandas minimap2 racon openpyxl -y

# Install BLAST+ and other dependencies
echo "Installing BLAST+..."
conda install -c bioconda blast -y

# Install XlsxWriter via pip (since it's not available in Conda)
echo "Installing XlsxWriter via pip..."
pip install XlsxWriter

# Install Snakemake (optional)
echo "Installing Snakemake..."
conda install -c bioconda snakemake -y

# Final message
echo "Installation complete! All required tools have been installed in the active Conda environment."
echo "You can now place your raw FASTQ files in the 'data/raw/' directory and run the pipeline with:"
echo "snakemake --cores 4"