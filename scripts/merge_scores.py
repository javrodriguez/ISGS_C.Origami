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
    
    # Find all bedgraph files and process them directly
    find_cmd = f"find {input_dir} -path '*/screening/bedgraph/*_impact_score.bedgraph'"
    print(f"Running command: {find_cmd}")
    bedgraph_files = subprocess.check_output(find_cmd, shell=True).decode().strip().split('\n')
    print(f"Found {len(bedgraph_files)} bedgraph files")
    
    # Process files and write to output
    with open('impact_scores.csv', 'w') as outfile:
        line_count = 0
        for file_path in bedgraph_files:
            try:
                # Extract peak ID from directory structure
                path = Path(file_path)
                peak_id = path.parent.parent.name.split('_')[1]
                
                # Read and process the bedgraph file
                with open(file_path, 'r') as infile:
                    line = infile.readline().strip()
                    if line:
                        outfile.write(f"{line}\t{peak_id}\n")
                        line_count += 1
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
    
    print(f"Processed {line_count} lines")
    
    # Sort the final file
    sort_cmd = "sort -k1,1 -k2,2n impact_scores.csv > temp_sorted.txt && mv temp_sorted.txt impact_scores.csv"
    subprocess.run(sort_cmd, shell=True, check=True)
    
    # Count the number of peaks processed
    wc_cmd = "wc -l impact_scores.csv"
    num_peaks = int(subprocess.check_output(wc_cmd, shell=True).decode().split()[0])
    
    print(f"Results saved to impact_scores.csv")
    print(f"Processed {num_peaks} peaks")

if __name__ == "__main__":
    main() 