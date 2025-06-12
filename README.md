# ISGS_C.Origami

A tool for performing in silico genome screening using C.Origami deep learning models.

## Description

ISGS_C.Origami is a computational tool designed for performing in silico genome screening using C.Origami deep learning models. It allows for efficient processing of genomic regions and prediction of their properties.

## Features

- Batch processing of genomic regions
- Support for multiple input formats
- Efficient parallel processing using SLURM
- Detailed timing and performance tracking
- Integration with C.Origami deep learning models

## How It Works

The script processes genomic regions in a hierarchical manner to efficiently handle large datasets:

1. **Chunking**:
   - The input BED file is split into chunks of 10,000 regions each
   - Each chunk is processed independently to manage memory efficiently
   - Example: A 155,000 region file will be split into 16 chunks (15 full chunks + 1 partial)

2. **Batching**:
   - Each chunk is further divided into batches of 1,000 regions
   - Batches are processed sequentially within each chunk
   - Example: A 10,000 region chunk will be processed in 10 batches

3. **Job Processing**:
   - Each batch is submitted as a SLURM array job
   - Jobs within a batch run in parallel
   - The script tracks the completion of each batch before proceeding
   - Timing information is recorded for each batch and the overall process

4. **Output**:
   - Results are saved in the specified output directory
   - A timing CSV file records the duration of each batch and the total process
   - Log files track the progress and any errors

## Usage

1. Prepare your input bed file with genomic regions
2. Run the screening script:
```bash
sbatch job_scheduler.sh input.bed output_directory
```

## Directory Structure

```
ISGS_C.Origami/
├── scripts/           # Main processing scripts
├── models/           # Model files and configurations
├── data/             # Data processing utilities
├── logs/             # Log files
└── tests/            # Test files
```

## Requirements

- SLURM workload manager
- CUDA-compatible GPU (for model inference)

## License

[Add your chosen license here]

## Contact

[Add your contact information here] 