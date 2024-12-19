import os
import subprocess

# Step 1: Get input and output directories
input_dir = input("Enter the path to the input directory containing .fasta files: ").strip()
output_dir = input("Enter the path to the output directory for results: ").strip()

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Step 2: Process each .fasta file in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".fasta") and file_name.startswith("centroid_"):
        # Extract the suffix from the filename after 'centroids_'
        sample_suffix = file_name.split("centroid_")[1].split(".fasta")[0]

        # Define paths for overlap and polished files with the specified prefixes
        fasta_path = os.path.join(input_dir, file_name)
        overlap_path = os.path.join(output_dir, f"overlap_{sample_suffix}.paf")
        polished_path = os.path.join(output_dir, f"polished_{sample_suffix}.fasta")

        # Step 3: Run minimap2 to generate overlaps
        minimap2_cmd = f"minimap2 -x ava-ont {fasta_path} {fasta_path} > {overlap_path}"
        print(f"Running minimap2 for {sample_suffix}...")
        subprocess.run(minimap2_cmd, shell=True, check=True)

        # Step 4: Run racon to polish based on overlaps
        racon_cmd = f"racon {fasta_path} {overlap_path} {fasta_path} > {polished_path}"
        print(f"Running racon for {sample_suffix}...")
        subprocess.run(racon_cmd, shell=True, check=True)

        print(f"Polishing complete for {sample_suffix}. Output saved to {polished_path}\n")

print("All .fasta files processed.")
