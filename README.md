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

Specify the number of workers NA (= number of age groups) and the number of time steps NT with the command
```
mpiexec -n NA python cohort_parallel/simulator.py --nt NT
```
By default, each task will take 0.015 sec per time step. A task can have up to NA time steps -- the worker takes other tasks to cover the number of time steps NT. 

A full set of options is
```
python cohort_parallel/simulator.py -h
usage: simulator.py [-h] --nt NT [-s STEP_TIME] [--ndata NDATA]

Run a simulation

options:
  -h, --help            show this help message and exit
  --nt NT               number of time steps
  -s STEP_TIME, --step-time STEP_TIME
                        (default: 0.015)
  --ndata NDATA         (default: 10000)
```

## Example

```
mpiexec -n 4 python cohort_parallel/simulator.py --nt 8
step        0    1    2    3 
-----------------------------
       0    0    1    2    3 
       1    0    1    2    4 
       2    0    1    5    4 
       3    0    6    5    4 
       4    7    6    5    4 
       5    7    6    5    8 
       6    7    6    9    8 
       7    7   10    9    8 
Elapsed time: 0.15 secs
Speedup: 3.10x (best case would be 4)
```
The table displays the steps (rows) and the corresponding tasks executed by each worker (columns). For instance, worker 0 executes tasks 0 (step = 0...3) and task 7 (steps 4...7).

Each step takes 0.015 seconds to execute. Since there are NT * NA steps, the total execution time 8 * 4 * 0.015 = 0.48 secs in this case. The wall clock time is 0.15 secs, corresponding to a speedup of 0.48/0.15 = 3.2 for 4 processes.


