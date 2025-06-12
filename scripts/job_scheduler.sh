#!/bin/bash
#SBATCH -J jobScheduler
#SBATCH --partition=gpu8_long
#SBATCH --mem=2gb 
#SBATCH --output=logs-job_scheduler/%J.logout
#SBATCH --error=logs-job_scheduler/%J.logerr

# Record overall start time
overall_start_time=$(date +%s)

BEDFILE=$1
OUTDIR=$2
CHUNK_SIZE=50  # Number of peaks per chunk

# Create output directory if it doesn't exist
mkdir -p "${OUTDIR}"

# Create timing log file
echo "Chunk,Start Time,End Time,Duration (seconds)" > "${OUTDIR}/chunk_timing.csv"

# Calculate total number of peaks and chunks
total_peaks=$(wc -l < "$BEDFILE")
num_chunks=$(( (total_peaks + CHUNK_SIZE - 1) / CHUNK_SIZE ))

echo "Processing $total_peaks peaks in $num_chunks chunks of $CHUNK_SIZE peaks each"

# Split the bed file into chunks
split -l $CHUNK_SIZE -d $BEDFILE bed_chunk_

# Submit all chunks in parallel
for chunk in bed_chunk_*; do
    # Record chunk start time
    chunk_start_time=$(date +%s)
    
    # Submit the chunk processing job
    JOB=$(sbatch --mem=10gb \
                 --time=28-00:00:00 \
                 --partition=gpu8_long \
                 run_screen.sh "$chunk" "${OUTDIR}" | awk '{print $4}')
    
    echo "Submitted chunk $chunk with job ID $JOB"
    
    # Store job ID and chunk name for later tracking
    echo "$JOB,$chunk,$chunk_start_time" >> "${OUTDIR}/chunk_jobs.csv"
done

echo "All chunks submitted. Waiting for completion..."

# Wait for all chunks to complete
while true; do
    # Check if any jobs are still running
    running_jobs=$(squeue -u $USER | grep -v "COMPLETED\|FAILED\|CANCELLED" | wc -l)
    if [ "$running_jobs" -eq 0 ]; then
        break
    fi
    echo "Still running: $running_jobs jobs"
    sleep 30
done

# Record overall end time and calculate total duration
overall_end_time=$(date +%s)
total_duration=$((overall_end_time - overall_start_time))

# Process timing information for each chunk
while IFS=, read -r job_id chunk_name start_time; do
    end_time=$(sacct -j $job_id --format=End --noheader)
    end_timestamp=$(date -d "$end_time" +%s)
    duration=$((end_timestamp - start_time))
    echo "$chunk_name,$start_time,$end_timestamp,$duration" >> "${OUTDIR}/chunk_timing.csv"
done < "${OUTDIR}/chunk_jobs.csv"

# Add total duration to timing log
echo "TOTAL,${overall_start_time},${overall_end_time},${total_duration}" >> "${OUTDIR}/chunk_timing.csv"

echo "Total execution time: ${total_duration} seconds" 