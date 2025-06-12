#!/bin/bash
#SBATCH -J jobScheduler
#SBATCH --partition=cpu_short
#SBATCH --mem=2gb 
#SBATCH --output=logs-cpu/%J.logout
#SBATCH --error=logs-cpu/%J.logerr

# Record overall start time
overall_start_time=$(date +%s)

BEDFILE=$1
OUTDIR=$2
CHUNK_SIZE=400  # Number of peaks per chunk

# Get the absolute path to the scripts directory
SCRIPT_DIR="/gpfs/home/rodrij92/BALL_Corigami/ISGS_C.Origami/scripts"
RUN_SCREEN_SCRIPT="${SCRIPT_DIR}/run_screen.sh"

# Debug information
echo "Current directory: $(pwd)"
echo "BEDFILE: $BEDFILE"
echo "OUTDIR: $OUTDIR"
echo "Script directory: $SCRIPT_DIR"
echo "Run screen script: $RUN_SCREEN_SCRIPT"
echo "Chunk size: $CHUNK_SIZE peaks"

# Verify script exists
if [ ! -f "$RUN_SCREEN_SCRIPT" ]; then
    echo "ERROR: Run screen script not found at $RUN_SCREEN_SCRIPT"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "${OUTDIR}"
mkdir -p "logs-cpu"

# Create timing log file
echo "Chunk,Start Time,End Time,Duration (seconds)" > "${OUTDIR}/chunk_timing.csv"

# Calculate total number of peaks and chunks
total_peaks=$(wc -l < "$BEDFILE")
num_chunks=$(( (total_peaks + CHUNK_SIZE - 1) / CHUNK_SIZE ))

echo "Processing $total_peaks peaks in $num_chunks chunks of $CHUNK_SIZE peaks each"

# Split the bed file into chunks inside the output directory
split -l $CHUNK_SIZE -d $BEDFILE "${OUTDIR}/bed_chunk_"

# Submit one job per chunk (no array jobs)
for chunk in ${OUTDIR}/bed_chunk_*; do
    chunk_start_time=$(date +%s)
    chunk_abs_path="$(pwd)/$chunk"
    echo "Submitting chunk: $chunk_abs_path"
    JOB=$(sbatch --mem=2gb \
                 --time=12:00:00 \
                 --partition=cpu_short \
                 --export=ALL \
                 "$RUN_SCREEN_SCRIPT" "$chunk_abs_path" "${OUTDIR}" | awk '{print $4}')
    if [ -z "$JOB" ]; then
        echo "ERROR: Failed to submit job for chunk $chunk"
        continue
    fi
    echo "Submitted chunk $chunk with job ID $JOB"
    echo "$JOB,$chunk,$chunk_start_time" >> "${OUTDIR}/chunk_jobs.csv"
done

echo "All chunks submitted. Waiting for completion..."
while true; do
    running_jobs=$(squeue -u $USER | grep -v "COMPLETED\|FAILED\|CANCELLED" | wc -l)
    if [ "$running_jobs" -eq 0 ]; then
        break
    fi
    echo "Still running: $running_jobs jobs"
    sleep 30
done

overall_end_time=$(date +%s)
total_duration=$((overall_end_time - overall_start_time))
while IFS=, read -r job_id chunk_name start_time; do
    end_time=$(sacct -j $job_id --format=End --noheader)
    end_timestamp=$(date -d "$end_time" +%s)
    duration=$((end_timestamp - start_time))
    echo "$chunk_name,$start_time,$end_timestamp,$duration" >> "${OUTDIR}/chunk_timing.csv"
done < "${OUTDIR}/chunk_jobs.csv"
echo "TOTAL,${overall_start_time},${overall_end_time},${total_duration}" >> "${OUTDIR}/chunk_timing.csv"
echo "Total execution time: ${total_duration} seconds" 