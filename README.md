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
Each task will take 1 sec per time step. A task can have up to NA time steps. 

## Example

```
time mpiexec -n 4 python cohort_parallel/simulator.py --nt 8
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

real    0m9.166s
user    0m3.111s
sys 0m0.672s
```
The table displays the steps (rows) and the corresponding tasks executed by each worker (columns). For instance, worker 0 executes tasks 0 (step = 0...3) and task 7 (steps 4...7).

Each step takes 1 second to execute. Since there are NT * NA steps, the total execution time 8 * 4 = 32 in this case. The wall clock time was 9.2 sec, corresponding to a speedup of 32/9.2 = 3.5  for 4 processes.


