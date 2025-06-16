#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: merge_scores.py <input_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    
    print(f"Processing bedgraph files in {input_dir}...")
    
    # Debug: Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist")
        sys.exit(1)
    
    # Debug: List peak directories
    peak_dirs_cmd = f"ls -d {input_dir}/PEAK_*"
    print(f"Running command: {peak_dirs_cmd}")
    peak_dirs = subprocess.check_output(peak_dirs_cmd, shell=True).decode().strip().split('\n')
    print(f"Found {len(peak_dirs)} peak directories")
    
    # First, concatenate all bedgraph files
    cat_cmd = f"cat {input_dir}/PEAK_*/screening/bedgraph/*_impact_score.bedgraph > temp_merged.txt"
    print(f"Running command: {cat_cmd}")
    try:
        subprocess.run(cat_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running cat command: {e}")
        sys.exit(1)
    
    # Debug: Check if temp file was created and has content
    if not os.path.exists('temp_merged.txt'):
        print("Error: temp_merged.txt was not created")
        sys.exit(1)
    
    file_size = os.path.getsize('temp_merged.txt')
    print(f"Size of temp_merged.txt: {file_size} bytes")
    
    # Create a mapping of file paths to peak IDs
    path_to_peak = {}
    for peak_dir in peak_dirs:
        peak_id = Path(peak_dir).name.split('_')[1]
        bedgraph_path = os.path.join(peak_dir, 'screening', 'bedgraph', '*_impact_score.bedgraph')
        # Get the actual bedgraph file path
        try:
            bedgraph_file = subprocess.check_output(f"ls {bedgraph_path}", shell=True).decode().strip()
            path_to_peak[bedgraph_file] = peak_id
        except subprocess.CalledProcessError:
            continue
    
    print(f"Created mapping for {len(path_to_peak)} bedgraph files")
    
    # Process the merged file and add peak IDs
    with open('temp_merged.txt', 'r') as infile, open('impact_scores.csv', 'w') as outfile:
        line_count = 0
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) == 4:  # Ensure we have all expected columns
                chrom, start, end, score = parts
                # Find the matching peak ID by checking the file path
                for file_path, peak_id in path_to_peak.items():
                    if f"{chrom}_{start}_{end}" in file_path:
                        outfile.write(f"{line.strip()}\t{peak_id}\n")
                        line_count += 1
                        break
        print(f"Processed {line_count} lines from temp_merged.txt")
    
    # Sort the final file
    sort_cmd = "sort -k1,1 -k2,2n impact_scores.csv > temp_sorted.txt && mv temp_sorted.txt impact_scores.csv"
    subprocess.run(sort_cmd, shell=True, check=True)
    
    # Count the number of peaks processed
    wc_cmd = "wc -l impact_scores.csv"
    num_peaks = int(subprocess.check_output(wc_cmd, shell=True).decode().split()[0])
    
    # Clean up temporary file
    os.remove('temp_merged.txt')
    
    print(f"Results saved to impact_scores.csv")
    print(f"Processed {num_peaks} peaks")

if __name__ == "__main__":
    main() 