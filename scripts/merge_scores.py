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
    
    # First, concatenate all bedgraph files
    cat_cmd = f"cat {input_dir}/PEAK_*/screening/bedgraph/*_impact_score.bedgraph > temp_merged.txt"
    subprocess.run(cat_cmd, shell=True, check=True)
    
    # Get list of all peak directories and their IDs
    peak_dirs = subprocess.check_output(f"ls -d {input_dir}/PEAK_*", shell=True).decode().strip().split('\n')
    peak_ids = {Path(d).name.split('_')[1]: d for d in peak_dirs}
    
    # Process the merged file and add peak IDs
    with open('temp_merged.txt', 'r') as infile, open('impact_scores.csv', 'w') as outfile:
        for line in infile:
            # Extract the file path from the bedgraph filename
            # The filename contains the coordinates that match the directory structure
            parts = line.strip().split('\t')
            if len(parts) == 4:  # Ensure we have all expected columns
                chrom, start, end, score = parts
                # Find the matching peak directory by checking the coordinates
                for peak_id, peak_dir in peak_ids.items():
                    if f"{chrom}_{start}_{end}" in peak_dir:
                        outfile.write(f"{line.strip()}\t{peak_id}\n")
                        break
    
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