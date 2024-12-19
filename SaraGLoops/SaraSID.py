# Blasts a fasta file against a Reference Sequences Library, parses the results, and creates a result Excel file

# Packages
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import SearchIO
from Bio import SeqIO
import pandas as pd
import xlsxwriter
from operator import itemgetter
import os
import glob

# USER VARIABLES
input_directory = input("Insert directory containing 'polished' files: ")  # directory with polished files
output_directory = input("Insert directory to save output files (or press Enter for default 'output_files'): ") or 'output_files'
ref_library = "ref_library"  # fixed library name
cutoff_pident = 98  # fixed percent identity cut-off in BLAST
intersp_div = 100  # fixed interspecific divergence

# Create the output directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Process each polished file
for input_file in glob.glob(os.path.join(input_directory, "polished_*.fasta")):
    print(f"Processing file: {input_file} against reference library: {ref_library}.fasta")

    # SECOND STEP: run the local BLAST
    cline = NcbiblastnCommandline(query=input_file, db=ref_library,
                                  evalue=0.001, max_target_seqs=150,
                                  perc_identity=cutoff_pident, out=input_file + ".txt",
                                  outfmt="6 std qlen slen gaps qcovs")
    print(cline)
    cline()  # Execute blast command line

    # THIRD STEP: parse the local blast result
    best_blasts = []  # Create an empty blast result list
    my_fields = "qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen gaps qcovs"
    QueryResults = SearchIO.parse(input_file + ".txt", "blast-tab", fields=my_fields)

    for QueryResult in QueryResults:
        to_sort = []  # Create an empty list to load the hits for each blast search
        for hit in QueryResult.hits:
            for hsp in hit.hsps:
                qcov = (hsp.query_end - hsp.query_start) / QueryResult.seq_len * 100  # Calculate query coverage
                if (qcov >= 75) or (hsp.aln_span > 0.9 * hit.seq_len):
                    # Check for alignment length, in case of very short queries/subjects
                    to_sort.append((QueryResult.id, hsp.ident_pct, hit.id, qcov, QueryResult.seq_len, hit.seq_len,
                                    hsp.aln_span, hsp.evalue))
        # Sort hits by %id in descending order
        sorted_by_perc_id = sorted(to_sort, reverse=True, key=itemgetter(1))  
        if len(sorted_by_perc_id) != 0:
           best_blasts.append(sorted_by_perc_id[0])  # Keep the first result

    # Load the blast result list into a DataFrame
    df = pd.DataFrame(best_blasts, columns=("query", "%id", "best_match", "%qcov", "qlen", "slen", "aln_len", "evalue"))

    print("Parsing completed!")

    # Load additional info from Check_tags.csv if it exists
    path = "./Check_tags.csv"
    if os.path.isfile(path):  # Check if the file exists 
        check_tags = pd.read_csv(path, sep=None, engine="python")

    df["notes"] = ""  # Add the empty notes column to the results DataFrame
    df_notes = []
    qry_to_check = []
    
    for qry, pid, sp, qc in zip(df["query"], df["%id"], df["best_match"], df["%qcov"]):
        if (pid < (100 - intersp_div)) or (qc < 75):
            note = "to_check"
            qry_to_check.append(qry)
        else:
            note = ""
            if os.path.isfile(path):
                for lab, tag in zip(check_tags["Label"], check_tags["Check_tag"]):
                    if lab in sp:
                        note = tag
        df_notes.append(note)
    df["notes"] = df_notes

    # Saving blast results for results labeled to_check
    df_to_check = pd.DataFrame(columns=["query", "%id", "best_match", "%qcov", "qlen", "slen", "aln_len", "evalue"])
    all_blast = pd.read_csv(input_file + ".txt", sep="\t", names=my_fields.split(), index_col=None)
    
    for check in qry_to_check:
        check_qry = all_blast[all_blast["qseqid"] == check]
        check_qry = check_qry.sort_values(by="%id", ascending=False)
        df_to_check = pd.concat([df_to_check, check_qry], ignore_index=True)

    if not df_to_check.empty:
        df_to_check = df_to_check[["qseqid", "pident", "sseqid", "qcovs", "qlen", "slen", "length", "evalue"]]

    # General statistics and counts
    data_lineage = {}  # Create an empty data statistics dictionary
    keys = []  # List of RSL taxa

    # Create an empty dictionary with all the species lineages from the Reference Sequences Library + Outgroup
    with open(ref_library + ".fasta", "r") as fasta:
        for k in SeqIO.parse(fasta, "fasta"):
            keys.append(k.id)
        keys.append("Results %id <" + str(cutoff_pident))
    
    for key in keys:
        data_lineage[key] = []  # Initialize the lists for each key

    # Store all the codes in the input fasta to count the outgroups
    samples = []
    with open(input_file, "r") as fasta:
        for sam in SeqIO.parse(fasta, "fasta"):
            samples.append(sam.id)

    outgroup = [sample for sample in samples if sample not in df["query"].values.tolist()]  # Counts how many samples without blast result

    # Search for the keys in the blast result list and append the sample identifier (qr) to that key
    for qr, pi, tax, cov, qln, sln, aln, evl in best_blasts:
        # Add the best match query to the corresponding lineage in data_lineage
        data_lineage[tax].append(qr)

    data_lineage["Results %id <" + str(cutoff_pident)] = outgroup

    # Debugging output to check the structure of data_lineage
    print("Data Lineage Structure:")
    print(data_lineage)

    # Ensure data_lineage is structured properly for DataFrame creation
    df_lineage = pd.DataFrame.from_dict(data_lineage, orient="index").reset_index()
    df_lineage.rename(columns={"index": "Lineages", 0: "Sequences"}, inplace=True)

    # Counts how many sequences (lineages) are in the Reference Sequences Library
    n_fasta = len([1 for line in open(input_file) if line.startswith(">")])

    # Calculate counts for output
    n_taxa = len(data_lineage) - 1  # Counts of taxa. Remove 1 because of "Results %id<cut-off"
    df_stats = pd.DataFrame({
        "Stats": ["Total taxa RSL", "Total input sequences"],
        "n": [n_taxa, n_fasta]
    })

    # FIFTH STEP: Excel with results creation
    excel_output_file = os.path.join(output_directory, os.path.basename(input_file).replace("polished_", "Results_").replace(".fasta", ".xlsx"))  # Save in new directory
    with pd.ExcelWriter(excel_output_file) as writer:
        df.to_excel(writer, index=False, sheet_name="Best_blast")
        df_to_check.to_excel(writer, index=False, sheet_name="Results_to_check")
        df_lineage.to_excel(writer, index=False, sheet_name="Lineages")
        df_stats.to_excel(writer, index=False, sheet_name="Summary")

        # Formatting
        workbook = writer.book
        format1 = workbook.add_format({"num_format": "0.0"})
        format2 = workbook.add_format({"num_format": "0.00E+00"})
        format3 = workbook.add_format({"bg_color": "red"})
        format4 = workbook.add_format({"align": "left"})

        worksheet1 = writer.sheets["Best_blast"]
        worksheet1.set_column("B:B", None, format1)  # %id and qcov in float format .1f
        worksheet1.set_column("D:D", None, format1)
        worksheet1.set_column("H:H", None, format2)  # evalue in scientific format

