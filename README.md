# cohort_parallel
A toy problem showing how to parallelise the SEAPODYM code along cohorts

## How to install the code

You need:
 * python 3.x
 * MPI
 * mpi4py
 * defopt

Type 
```
pip install mpi4py defopt
```
to install the packages. Then type
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
Worker    0
===========
     0 |    0    2 
     1 |    0    2 
     2 |    0    5 
     3 |    0    5 
     4 |    7    5 
     5 |    7    5 
     6 |    7    9 
     7 |    7    9 
Worker    1
===========
     0 |    1    3 
     1 |    1    4 
     2 |    1    4 
     3 |    6    4 
     4 |    6    4 
     5 |    6    8 
     6 |    6    8 
     7 |   10    8 
Elapsed time: 0.270 secs
Speedup: 1.776x (best case would be 2)
```
The tables display the steps (rows) and the corresponding tasks executed by each worker. For instance, worker 0 executes tasks 0 (step = 0-3), task 7 (steps 4-7), task 2 (steps 0-1), task 5 (steps 2-5) and task 9 (steps 6-7).

Each step takes 0.015 seconds to execute. Since there are NT * NA steps, the total execution time 8 * 4 * 0.015 = 0.48 secs in this case. The wall clock time is 0.270 secs, which corresponds to a speedup of 0.48/0.27 = 1.78 for 2 processes.


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
Elapsed time: 1.599 secs
Speedup: 34.718x (best case would be 37)
```

You can adjust the number of workers (and other SLURM options) by passing "--ntasks NUM_WORKERS" to the "sbatch" command. The number of time steps, the number of age groups and the number of data values to exchange between each pair of workers can be set by passing the "-t NUM_STEPS", "-a NUM_AGE_GROUPS" and "-d NDATA" options to the SLURM script. For instance,
```
sbatch --ntasks=100 --nodes=2 slurm/simulator.sh -t 200 -a 40 -d 10000
```








