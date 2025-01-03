import os
import csv

def calculate_file_average(file_path):
    """Calculate the average depth and number of lines in a single file"""
    total_depth = 0
    total_length = 0

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 3:
                continue
            try:
                depth = int(parts[2])  #  Extract depth value
                total_depth += depth
                total_length += 1
            except ValueError:
                continue

    if total_length == 0:
        return 0, 0  
    return round(total_depth / total_length,3), total_length

    

def process_all_files(root_dir, output_file, label):
    """Function 1: Process all files and calculate the average depth of each file"""
    results = []

    for sample_id in os.listdir(root_dir):  # Iterate through all sample folders
        sample_dir = os.path.join(root_dir, sample_id)
        if not os.path.isdir(sample_dir):
            continue

        for file_name in os.listdir(sample_dir):  # Iterate through files in each sample folder
            file_path = os.path.join(sample_dir, file_name)
            if not os.path.isfile(file_path):
                continue

            # Extract core part of the file as a label (remove prefix and suffix)
            core_name = file_name.replace(f"{sample_id}_", "").replace(".txt", "")

            avg_depth, length = calculate_file_average(file_path)
            results.append({
                "Sample_ID": sample_id,
                "Depth_File": core_name,
                "Average_Depth": avg_depth,
                "Length": length,
                "Label": label
            })

    # Write results to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Sample_ID", "Depth_File", "Average_Depth", "Length", "Label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Function 1 results saved to: {output_file}")


def process_selected_files(root_dir, output_file, label, selected_files):
    """Function 2: Process only selected files and calculate their average depth"""
    results = []

    for sample_id in os.listdir(root_dir):  # Iterate through all sample folders
        sample_dir = os.path.join(root_dir, sample_id)
        if not os.path.isdir(sample_dir):
            continue

        for file_name in os.listdir(sample_dir):  # Iterate through files in each sample folder
            file_path = os.path.join(sample_dir, file_name)
            if not os.path.isfile(file_path):
                continue

            # Extract core part of the file as a label (remove prefix and suffix)
            core_name = file_name.replace(f"{sample_id}_", "").replace(".txt", "")

            # Check if file is in the selected list
            if core_name not in selected_files:
                continue

            avg_depth, length = calculate_file_average(file_path)
            results.append({
                "Sample_ID": sample_id,
                "Depth_File": core_name,
                "Average_Depth": avg_depth,
                "Length": length,
                "Label": label
            })

    # Write results to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Sample_ID", "Depth_File", "Average_Depth", "Length", "Label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Function 2 results saved to: {output_file}")


def process_multiple_files_with_label(root_dir, output_file, label, selected_files, custom_label):
    """Function 3: Process multiple selected files and calculate the combined average depth (rounded to 3 decimals)"""
    results = []

    for sample_id in os.listdir(root_dir):  # Iterate through all sample folders
        sample_dir = os.path.join(root_dir, sample_id)
        if not os.path.isdir(sample_dir):
            continue

        # Store results for target files in the current sample
        sample_results = []

        for file_name in os.listdir(sample_dir):  # Iterate through files in each sample folder
            file_path = os.path.join(sample_dir, file_name)
            if not os.path.isfile(file_path):
                continue

            # Extract core part of the file as a label (remove prefix and suffix)
            core_name = file_name.replace(f"{sample_id}_", "").replace(".txt", "")

            # Check if file is in the selected list
            if core_name not in selected_files:
                continue

            avg_depth, length = calculate_file_average(file_path)
            sample_results.append({
                "Average_Depth": avg_depth,
                "Length": length
            })

        # Calculate overall average depth and total length for the current sample
        total_length = sum(r["Length"] for r in sample_results)
        if total_length > 0:
            total_avg_depth = sum(r["Average_Depth"] * r["Length"] for r in sample_results) / total_length
        else:
            total_avg_depth = 0

        results.append({
            "Sample_ID": sample_id,
            "Depth_File": custom_label,
            "Average_Depth": total_avg_depth,
            "Length": total_length,
            "Label": label
        })

    # Write results to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Sample_ID", "Depth_File", "Average_Depth", "Length", "Label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            # Format Average_Depth to 3 decimal places
            row["Average_Depth"] = round(row["Average_Depth"], 3)
            writer.writerow(row)

    print(f"Function 3 results saved to: {output_file}")

    

if __name__ == "__main__":
    #blood all_files blood
    process_all_files(
        root_dir="depth_results_exon_intron_blood_no_duplication",
        output_file="blood_all_BRD.csv",
        label="blood"
    )
    
    #tumor all_files
    process_all_files(
        root_dir="depth_results_exon_intron_tumor_no_duplication",
        output_file="tumor_all_BRD.csv",
        label="tumor"
    )

    #blood chr13_14_15_21_22_exon
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_blood_no_duplication",
        output_file="blood_chr13_14_15_21_22_exon_BRD.csv",
        label="blood",
        selected_files=["chr13_exon_depth", "chr14_exon_depth", "chr15_exon_depth", "chr21_exon_depth", "chr22_exon_depth"],
        custom_label="chr13_14_15_21_22_exon"
    )
    
    #tumor chr13_14_15_21_22_exon
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_tumor_no_duplication",
        output_file="tumor_chr13_14_15_21_22_exon_BRD.csv",
        label="tumor",
        selected_files=["chr13_exon_depth", "chr14_exon_depth", "chr15_exon_depth", "chr21_exon_depth", "chr22_exon_depth"],
        custom_label="chr13_14_15_21_22_exon"
    )

    #blood chr1_exon_intron
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_blood_no_duplication",
        output_file="blood_chr1_exon_intron.csv",
        label="blood",
        selected_files=["chr1_intron_depth", "chr1_exon_depth"],
        custom_label="chr1_exon_intron"
    )
    
    #tumor chr1_exon_intron
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_tumor_no_duplication",
        output_file="tumor_chr1_exon_intron.csv",
        label="tumor",
        selected_files=["chr1_intron_depth", "chr1_exon_depth"],
        custom_label="chr1_exon_intron"
    )



