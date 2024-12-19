#!/bin/bash

# Prompt the user for the input path
read -p "Enter the input path (e.g., /path/to/your/ugly/reads): " input_path

# Prompt the user for the output directory
read -p "Enter the output directory (e.g., /path/to/output): " output_dir

# Prompt the user for the file prefix
read -p "Enter the prefix for output files (e.g., myoutputname): " file_prefix

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through each FASTQ file in the input path
for file in ${input_path}/*.fastq; do
    # Extract sample ID from the filename
    sample_id=$(echo "$file" | sed 's/.*_\([0-9]*_[C0-9]*\)\.fastq/\1/')

    # Define the output file path
    output_file="${output_dir}/${file_prefix}_${sample_id}.fastq"

    # Debugging output
    echo "Processing the fucking file: $file"
    echo "Output fucking file will be: $output_file"

    # Run NanoFilt with specified parameters
    NanoFilt -q 10 -l 200 --maxlength 350 "$file" > "$output_file"
done

