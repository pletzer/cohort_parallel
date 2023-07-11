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
mpiexec -n NA python cohort_parallel/ex_run.py --nt NT
```
Each task will take 1 sec per time step. A task can have up to NA time steps. 

## Example

```
time mpiexec -n 4 python cohort_parallel/ex_run.py --nt 8
worker 2 executed tasks 2x2 5x4 9x2 
worker 0 executed tasks 0x4 7x4 
worker 1 executed tasks 1x3 6x4 10x1 
worker 3 executed tasks 3x1 4x4 8x3 

real	0m8.758s
user	0m1.495s
sys	0m0.436s
```
The number before "x" is the task ID and the number after the "x" is the number of time steps. Each time step takes 1 sec. In this particular case, worker 0 executed (rows are time steps and columns are age groups)
```
0 . . .
. 0 . .
. . 0 .
. . . 0
7 . . .
. 7 . .
. . 7 .
. . . 7
```
while worker 1 executed
```
. 1 . .
. . 1 .
. . . 1
6 . . .
. 6 . .
. . 6 .
. . . 6
10. . .
```
etc. The total execution cost is NA * NT, in this case 32 sec. The parallel speedup therefore is "32 sec/8.8 sec = 3.6". 

