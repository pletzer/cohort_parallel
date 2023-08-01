import numpy as np
from mpi4py import MPI
import defopt

from task_manager import TaskManager
from task import Task

import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)


def print_info(list_of_executed_tasks, na, nt, comm, worker_id):

    # send the info to root
    lets = comm.gather(list_of_executed_tasks, root=0)

    if worker_id == 0:

        for wid in range(len(lets)):
            print(f'Worker {wid}')
            print(f'==============')
            for step in range(nt):
                print(f'{step:6d} | ', end='')
                for tid in lets[wid][step]:
                    print(f'{tid:4d} ', end='')
                print()


def main(*, nt: int, na: int, step_time: float=0.015, ndata: int=10000):
    """
    Run a simulation

    :param nt: number of time steps
    :param na: number of age groups
    :param step_time: time it takes to execute one time step for one cohort in seconds
    :param ndata: number of doubles to accumulate at the end of each time step
    """

    # info about which tasks have been executed
    list_of_executed_tasks = {}

    comm = MPI.COMM_WORLD
    # worker ID = MPI rank
    worker_id = comm.Get_rank()
    num_workers = comm.Get_size()

    # data to send to other workers
    srcData = np.zeros((ndata,), np.float64)

    # data to receive from other workers
    rcvData = np.empty((ndata,), np.float64)
    rcvWin = MPI.Win.Create(rcvData, comm=comm)

    # assign tasks to workers
    tsk_manager = TaskManager(na, nt, num_workers)
    
    # get the initial tasks for this processing unit (worker)
    task_ids = tsk_manager.get_init_task_ids(worker_id)
    
    # generate the tasks
    tasks = [Task(tid, ndata) for tid in task_ids]

    # number of time steps for each cohort
    nts = [tsk_manager.get_num_steps(tid) for tid in task_ids]

    tic = MPI.Wtime()

    # advance in time
    for step in range(nt):

        list_of_executed_tasks[step] = []

        # tell MPI to prepare receiving data
        rcvWin.Fence(MPI.MODE_NOPUT | MPI.MODE_NOPRECEDE)

        # set the data to zero
        srcData[:] = 0

        # iterate over the tasks (cohorts) assigned to each worker
        for i in range(len(tasks)):

            tid = task_ids[i]

            # run one step
            tasks[i].execute_step(step_time)

            # sum the local contributions
            srcData += tasks[i].get_data()

            list_of_executed_tasks[step].append(tasks[i].get_task_id())

            # create a new task, if need be
            if tasks[i].get_local_step() == nts[i]:
                next_tid = tsk_manager.get_next_task(tid)
                tasks[i] = Task(next_tid, ndata)
                nts[i] = tsk_manager.get_num_steps(next_tid)

        # sum the contributions from all the workers
        rcvWin.Accumulate(srcData, target_rank=worker_id, op=MPI.SUM)

        rcvWin.Fence(MPI.MODE_NOSUCCEED)

    toc = MPI.Wtime()

    print_info(list_of_executed_tasks, na, nt, comm, worker_id)

    if worker_id == 0:
        elapsed_time = toc - tic
        print(f'Elapsed time: {elapsed_time:.3f} secs')
        print(f'Speedup: {na*nt*step_time/elapsed_time:.3f}x (best case would be {num_workers})')


if __name__ == '__main__':
    defopt.run(main)

    
