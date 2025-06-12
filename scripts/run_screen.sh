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

source /gpfs/home/rodrij92/home_abl/miniconda3/etc/profile.d/conda.sh
conda activate corigami_ball

# Process each peak in the chunk sequentially
while IFS=$'\t' read -r chr start end peak_id; do
    peak_length=$((end-start))
    echo "Processing peak $peak_id at $chr:$start-$end"
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
    echo "Completed peak $peak_id"
done < "$bedfile" 