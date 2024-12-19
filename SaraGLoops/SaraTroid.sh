#!/bin/bash

# Prompt the user for the input directory
read -p "Enter the input directory (where you have the trimmed sequences): " input_dir

# Prompt the user for the output directory
read -p "Enter the output directory (e.g., /path/to/output): " output_dir

# Create the centroids output directory
centroids_output_dir="${output_dir}/centroids"
mkdir -p "$centroids_output_dir"

# Check if there are any FASTQ files in the input directory
if compgen -G "${input_dir}/*.fastq" > /dev/null; then
    # Iterate over each FASTQ file in the input directory
    for file in "${input_dir}"/*.fastq; do
        # Extract the sample ID from the file name without the "trimmed_" prefix
        sample_id=$(basename "$file" | sed 's|^trimmed_||; s|\.fastq$||')
        
        # Create the output filename by adding "centroid_" to the sample ID
        output_file="${centroids_output_dir}/centroid_${sample_id}.fasta"
        
        # Run the vsearch command
        vsearch --cluster_fast "$file" --id 0.98 --centroids "$output_file"
        
        # Check if vsearch was successful
        if [ $? -eq 0 ]; then
            # Optional: Print a message indicating progress
            echo "Processed: $file -> $output_file"
        else
            echo "Error processing file: $file"
        fi
    done
else
    echo "No FASTQ files found in ${input_dir}"
fi

