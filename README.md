# cohort_parallel
A toy problem showing how to parallelise the SEAPODYM code along cohorts

## How to install the code

You need:
 * python 3.x
 * MPI
 * mpi4py
 * defopt

We recommend that you install the Python dependecies in a virtual environmen
```
python -mvenv venv
source venv/bin/activate
pip install numpy mpi4py defopt
```

Then type
```
pip install -e .
```
to install cohort_parallel.

## How to run the code

Specify the number of workers NW (= number of cores), the number of age groups (NA) and the number of time steps NT with the command
```
mpiexec -n NW python cohort_parallel/simulator.py --nt NT --na NA
```
By default, each task will take 0.015 sec per time step. A task can have up to NA time steps -- the worker takes other tasks to cover the number of time steps NT. 

A full set of options is
```
python cohort_parallel/simulator.py -h
```

## Example: interactive run

```
mpiexec -n 2 python cohort_parallel/simulator.py --na 4 --nt 8
```
The tables display the steps (rows) and the corresponding tasks executed by each worker (columns). For instance, worker 0 executes tasks 0 (step = 0-3) and task 7 (steps 4-7), as well as tasks 2 and 5.

Each step takes 0.015 seconds to execute. Since there are NT * NA steps, the total execution time 8 * 4 * 0.015 = 0.48 secs in this case. The wall clock time is 0.269 secs, which corresponds to a speedup of 0.48/0.269 = 1.787 for 2 processes.


## Example:  submit job to NeSI's mahuika platform

Make sure you have "defopt" installed,
```
module load Python
pip install defopt --user
```
(You only need to do this once.)

Then type
```
sbatch slurm/simulator.sh
```
to submit the job. This will print something like
```
Submitted batch job JOBID
```
Record the job id JOBID returned by the above command. You can check progress of the job's execution with
```
squeue --me
```

Typing
```
tail cohort_parallel_JOBID.out
```
(replacing JOBID with above job ID number) will returned something like
```
Elapsed time: 1.67 secs
Speedup: 33.18x (best case would be 37)
```

You can adjust the number of workers (and other SLURM options) by passing "--ntasks NUM_WORKERS" to the "sbatch" command. The number of time steps (NT), the number of age groups (NA) and the number of data values to exchange between each pair of workers can be set by passing the "-t NT", "-a NA" and "-d NDATA" options to the SLURM script. For instance,
```
sbatch --ntasks=50 --nodes=2 slurm/simulator.sh -t 200 -a 100 -d 10000
```








