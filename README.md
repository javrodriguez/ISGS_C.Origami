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