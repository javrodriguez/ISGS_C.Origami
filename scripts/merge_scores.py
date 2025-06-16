#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def extract_peak_id(path):
    """Extract peak ID from directory path."""
    try:
        # Get the parent directory of the bedgraph directory
        parent_dir = path.parent.parent
        # Get the peak directory name (e.g., PEAK_12588)
        peak_dir = parent_dir.name
        # Extract the number after PEAK_
        if peak_dir.startswith('PEAK_'):
            return peak_dir[5:]  # Remove 'PEAK_' prefix
        print(f"Warning: Unexpected directory format: {peak_dir}")
        return None
    except Exception as e:
        print(f"Error extracting peak ID from {path}: {str(e)}")
        return None

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
        error_count = 0
        for file_path in bedgraph_files:
            try:
                # Extract peak ID from directory structure
                path = Path(file_path)
                peak_id = extract_peak_id(path)
                
                if peak_id is None:
                    error_count += 1
                    continue
                
                # Read and process the bedgraph file
                with open(file_path, 'r') as infile:
                    line = infile.readline().strip()
                    if line:
                        outfile.write(f"{line}\t{peak_id}\n")
                        line_count += 1
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                error_count += 1
                continue
    
    print(f"Processed {line_count} lines successfully")
    if error_count > 0:
        print(f"Encountered {error_count} errors")
    
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