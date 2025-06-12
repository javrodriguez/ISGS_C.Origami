# ISGS (In Silico Genome Screening)

A tool for performing in silico genome screening using deep learning models.

## Description

ISGS is a computational tool designed for performing in silico genome screening using deep learning models. It allows for efficient processing of genomic regions and prediction of their properties.

## Features

- Batch processing of genomic regions
- Support for multiple input formats
- Efficient parallel processing using SLURM
- Detailed timing and performance tracking
- Integration with deep learning models

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ISGS.git
cd ISGS
```

2. Create a conda environment:
```bash
conda create -n isgs python=3.8
conda activate isgs
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your input bed file with genomic regions
2. Run the screening script:
```bash
sbatch job_scheduler.sh input.bed output_directory
```

## Directory Structure

```
ISGS/
├── scripts/           # Main processing scripts
├── models/           # Model files and configurations
├── data/             # Data processing utilities
├── logs/             # Log files
└── tests/            # Test files
```

## Requirements

- Python 3.8+
- SLURM workload manager
- CUDA-compatible GPU (for model inference)

## License

[Add your chosen license here]

## Contact

[Add your contact information here] 