#!/bin/bash -e
#SBATCH --job-name=cohort_parallel # job name (shows up in the queue)
#SBATCH --time=00:10:00      # Walltime (HH:MM:SS)
#SBATCH --ntasks=37
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --partition=milan

ml purge
ml Python

nt="100"
ndata="24000"
while getopts u:a:f: flag
do
    case "${flag}" in
        t) nt=${OPTARG};;
        d) ndata=${OPTARG};;
    esac
done

echo "Number of workers: ${SLURM_NTASKS}"
echo "Running the simulator for $nt steps and exchanging $ndata doubles"
srun python cohort_parallel/simulator.py --nt $nt --ndata $ndata
