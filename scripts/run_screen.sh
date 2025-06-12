#!/bin/bash
#SBATCH -J screen
#SBATCH --mem=10gb 
#SBATCH --partition=gpu8_long
#SBATCH --output=logs-screen/%J.out
#SBATCH --error=logs-screen/%J.err

bedfile=$1
outdir=$2
model=/gpfs/data/abl/home/rodrij92/PROJECTS/BALL_Corigami/C.Origami/ball_stringent-oe_exp_pred_ep32.ckpt
seq=/gpfs/data/abl/home/rodrij92/PROJECTS/BALL_Corigami/C.Origami//data/hg38/dna_sequence
ctcf=/gpfs/data/abl/home/rodrij92/PROJECTS/BALL_Corigami/C.Origami/data/hg38/BALL-MCG017/genomic_features/ctcf_log2fc.bw
atac=/gpfs/data/abl/home/rodrij92/PROJECTS/BALL_Corigami/C.Origami/data/hg38/BALL-MCG017/genomic_features/atac.bw

# Debug information
echo "Processing array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "Input bed file: ${bedfile}"

# Read the line for this array task
line=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "${bedfile}")
if [ -z "$line" ]; then
    echo "ERROR: Could not read line ${SLURM_ARRAY_TASK_ID} from ${bedfile}"
    exit 1
fi

# Parse the line
chr=$(echo "$line" | cut -f1)
start=$(echo "$line" | cut -f2)
end=$(echo "$line" | cut -f3)
peak_id=$(echo "$line" | cut -f4)

if [ -z "$chr" ] || [ -z "$start" ] || [ -z "$end" ] || [ -z "$peak_id" ]; then
    echo "ERROR: Failed to parse line: $line"
    exit 1
fi

peak_length=$((end-start))

echo "Processing peak: $peak_id at $chr:$start-$end"

source /gpfs/home/rodrij92/home_abl/miniconda3/etc/profile.d/conda.sh
conda activate corigami_ball

corigami-screen --out ${outdir} \
                --celltype ${peak_id} \
                --chr ${chr} \
                --model ${model} \
                --seq ${seq} \
                --ctcf ${ctcf} \
                --atac ${atac} \
                --screen-start ${start} \
                --screen-end ${end} \
                --perturb-width ${peak_length} \
                --step-size ${peak_length} \
                --save-bedgraph \
                --padding zero \
                --save-frames 