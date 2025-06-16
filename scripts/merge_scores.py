#!/usr/bin/env python3

import os
import sys
import glob
import pandas as pd
from pathlib import Path

def extract_peak_id(file_path):
    """Extract peak ID from the directory structure."""
    # Convert to Path object for easier path manipulation
    path = Path(file_path)
    # Get the parent directory of the bedgraph directory
    parent_dir = path.parent.parent
    # Get the peak directory name and extract the ID
    peak_dir = parent_dir.name
    peak_id = peak_dir.split('_')[1]  # Assumes format PEAK_XXXXX
    return peak_id

def process_bedgraph_files(input_dir):
    """Process all bedgraph files and combine their data."""
    # Find all impact score bedgraph files
    pattern = os.path.join(input_dir, "**", "screening", "bedgraph", "*_impact_score.bedgraph")
    bedgraph_files = glob.glob(pattern, recursive=True)
    
    if not bedgraph_files:
        print(f"No bedgraph files found in {input_dir}")
        sys.exit(1)
    
    # List to store all data
    all_data = []
    
    # Process each bedgraph file
    for file_path in bedgraph_files:
        try:
            # Extract peak ID from directory structure
            peak_id = extract_peak_id(file_path)
            
            # Read the bedgraph file
            with open(file_path, 'r') as f:
                line = f.readline().strip()
                if line:
                    # Split the line into columns
                    chrom, start, end, impact_score = line.split('\t')
                    
                    # Add to our data list
                    all_data.append({
                        'chrom': chrom,
                        'start': int(start),
                        'end': int(end),
                        'impact_score': float(impact_score),
                        'peak_id': peak_id
                    })
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Sort by chromosome and start position
    df = df.sort_values(['chrom', 'start'])
    
    return df

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: merge_scores.py <input_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    
    # Process the files
    print(f"Processing bedgraph files in {input_dir}...")
    df = process_bedgraph_files(input_dir)
    
    # Save to CSV
    output_file = "impact_scores.csv"
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    print(f"Processed {len(df)} peaks")

if __name__ == "__main__":
    main() 