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
    
    # Find all impact score bedgraph files
    find_cmd = f"find {input_dir} -path '*/screening/bedgraph/*_impact_score.bedgraph'"
    
    print(f"Processing bedgraph files in {input_dir}...")
    
    # Create a temporary file to store the combined data
    temp_file = "temp_impact_scores.txt"
    
    try:
        # Use find to get all bedgraph files and process them
        with open(temp_file, 'w') as outfile:
            # Get list of files
            files = subprocess.check_output(find_cmd, shell=True).decode().strip().split('\n')
            
            if not files or files[0] == '':
                print(f"No bedgraph files found in {input_dir}")
                sys.exit(1)
            
            # Process each file
            for file_path in files:
                try:
                    # Extract peak ID from directory structure
                    path = Path(file_path)
                    peak_id = path.parent.parent.name.split('_')[1]
                    
                    # Read the bedgraph file and add peak_id
                    with open(file_path, 'r') as infile:
                        line = infile.readline().strip()
                        if line:
                            outfile.write(f"{line}\t{peak_id}\n")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    continue
        
        # Sort the combined file by chromosome and start position
        sort_cmd = f"sort -k1,1 -k2,2n {temp_file} > impact_scores.csv"
        subprocess.run(sort_cmd, shell=True, check=True)
        
        # Count the number of peaks processed
        wc_cmd = f"wc -l impact_scores.csv"
        num_peaks = int(subprocess.check_output(wc_cmd, shell=True).decode().split()[0]) - 1  # Subtract header
        
        print(f"Results saved to impact_scores.csv")
        print(f"Processed {num_peaks} peaks")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    main() 