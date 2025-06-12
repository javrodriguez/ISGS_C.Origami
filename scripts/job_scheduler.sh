#!/bin/bash
#SBATCH -J jobScheduler
#SBATCH --partition=gpu4_long,gpu8_long
#SBATCH --mem=2gb 
#SBATCH --output=logs-job_scheduler/%J.logout
#SBATCH --error=logs-job_scheduler/%J.logerr

# Record overall start time
overall_start_time=$(date +%s)

BEDFILE=$1
OUTDIR=$2
# Keep batch size at 1000 due to HPC limitations
BATCH_SIZE=1000
# Increased max index to reduce number of chunks
MAX_INDEX=10000

# Create output directory if it doesn't exist
mkdir -p "${OUTDIR}"

# Create timing log file
echo "Batch,Start Time,End Time,Duration (seconds)" > "${OUTDIR}/batch_timing.csv"

# Split the bed file into larger chunks
split -l $MAX_INDEX -d $BEDFILE bed_chunk_

for chunk in bed_chunk_*; do
    lines=$(wc -l < "$chunk")
    num_batches=$(( (lines + BATCH_SIZE - 1) / BATCH_SIZE ))

    for ((i=0; i<num_batches; i++)); do
        # Record batch start time
        batch_start_time=$(date +%s)
        
        start=$((i * BATCH_SIZE + 1))
        end=$(( (i + 1) * BATCH_SIZE ))
        [ "$end" -gt "$lines" ] && end=$lines

        # Submit job with increased memory and time limit
        JOB=$(sbatch --array=${start}-${end} \
                     --mem=10gb \
                     --time=2:00:00 \
                     run_screening_timed.sh "$chunk" "${OUTDIR}" | awk '{print $4}')
        
        echo "Submitted batch job with ID $JOB, waiting to complete..."
        
        # More efficient job status checking
        while true; do
            status=$(sacct -j $JOB --format=State --noheader | grep -v "COMPLETED\|FAILED\|CANCELLED" | wc -l)
            if [ "$status" -eq 0 ]; then
                break
            fi
            sleep 5  # Reduced sleep time
        done
        
        # Record batch end time and duration
        batch_end_time=$(date +%s)
        batch_duration=$((batch_end_time - batch_start_time))
        
        # Log batch timing
        echo "${chunk}_batch_${i},${batch_start_time},${batch_end_time},${batch_duration}" >> "${OUTDIR}/batch_timing.csv"
        
        echo "Completed batch ${i} of ${chunk} in ${batch_duration} seconds"
    done
done

# Record overall end time and calculate total duration
overall_end_time=$(date +%s)
total_duration=$((overall_end_time - overall_start_time))

# Add total duration to timing log
echo "TOTAL,${overall_start_time},${overall_end_time},${total_duration}" >> "${OUTDIR}/batch_timing.csv"

echo "Total execution time: ${total_duration} seconds" 