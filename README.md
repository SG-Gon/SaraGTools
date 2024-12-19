# ✨ Welcome to SaraGTool ✨

Welcome to SaraGTool! 🛠️ This repository is a compilation of various bioinformatics tools designed for working with raw Oxford Nanopore Technologies (ONT) sequencing reads. 📊🌿 It's optimized for Ubuntu systems and will help you process and analyze your ONT data with ease! 💻🔬
🧬 About SaraGMake 🧬

Within SaraGTool, you’ll find: 

## 🦠 SaraGMake: A powerful Snakemake pipeline specifically designed for subtyping _Blastocystis_ sp. from ONT raw reads. ✨

This tool automates the process of subtyping, making it easy to handle your ONT data and produce high-quality results. The pipeline uses Snakemake, an efficient workflow system for scalable data analysis. 🚀💾

## 🧩 SaraGLoops - Loops for ONT Read Processing 🔄

SaraGLoops is a collection of programs designed to prepare and process ONT reads for analysis. These programs automate the preparation steps, helping you streamline the analysis of raw ONT data using existing bioinformatics tools. Below are the components of SaraGLoops:

### 🔹 SaraGilt - Loop for NanoFilt 🧑‍🔬

SaraGilt automates the filtering of ONT reads using NanoFilt. It processes raw sequencing data, applying quality filters based on the desired read length and quality scores. This step ensures that only high-quality reads are used in subsequent analyses, improving the accuracy of downstream results.

### 🔹 SaraPlot - Loop for NanoPlot 📊

SaraPlot generates informative visualizations of your sequencing data using NanoPlot. This tool creates plots to assess the quality and distribution of read lengths, GC content, and other important statistics. These visualizations help you better understand your dataset and assess its suitability for further analysis.

### 🔹 SaraPolish - Loop for Racon 🧬

SaraPolish automates the Racon polishing process, improving the quality of your raw ONT reads by correcting errors. Racon uses the raw reads to generate more accurate consensus sequences, which are critical for downstream analysis and subtyping.

### 🔹 SaraSid - Loop using PARSID 🔍

SaraSid facilitates the use of PARSID (a tool for phylogenetic analysis of microbial diversity) by automating the workflow. It helps in processing and analyzing your ONT reads to classify based on a custom database efficiently. SaraSid integrates PARSID into your pipeline, allowing for easy subtyping and classification of your data.

### 🔹 SaraTroid - Loop for vsearch to Make Centroids 🔬

SaraTroid uses vsearch to cluster your raw ONT reads into centroids. This tool automates the process of generating representative sequences (centroids) from a set of sequences, which is essential for taxonomic classification and further analysis. By using vsearch, SaraTroid simplifies the process of grouping similar sequences, improving the efficiency of your analysis pipeline.

# 📝 Instructions 📖

All instructions for using the tools are located inside their respective folders. Each folder includes a README.md with detailed instructions on how to use the programs on that specific folder. 📂

