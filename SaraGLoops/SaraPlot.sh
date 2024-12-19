#!/bin/bash
# Display a message at the beginning
echo "
This step is to verify if we trimmed well the reads.
"

# Prompt the user for the input path
read -p "Enter the input (e.g., /path/to/trimmed/reads): " input_path

# Prompt the user for the output directory
read -p "Enter the output directory (e.g., /path/to/output): " output_dir

# Create the output directory if it doesn't exist
mkdir -p "$output_dir/NanoPlot_output"

# Flag to track if any FASTQ files are processed
files_processed=false

# Loop through each FASTQ file in the specified input path
for file in "$input_path"/*.fastq; do

      # Extract the sample ID from the filename (remove the .fastq extension)
    sample_id=$(basename "$file" .fastq)

    # Define the output directory for NanoPlot
    sample_output_dir="${output_dir}/NanoPlot_output/${sample_id}"

    # Create the sample output directory if it doesn't exist
    mkdir -p "$sample_output_dir"

    # Debugging output: Print the current file and output directory
    echo "Processing file: $file"
    echo "Output directory will be: $sample_output_dir"

    # Run NanoPlot with the specified parameters
    NanoPlot --fastq "$file" --outdir "$sample_output_dir" --prefix "nanoplot_report_${sample_id}"

    # Debugging output: Confirm that NanoPlot has been executed
    echo "NanoPlot executed for sample: ${sample_id}"
done


