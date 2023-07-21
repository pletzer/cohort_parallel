from mpi4py import MPI
import defopt
from worker import Worker

import sys
import logging
logging.basicConfig(format='%(asctime)s: %(message)s') #, level=logging.DEBUG)


def print_info(list_of_executed_tasks, na, nt, comm, worker_id):

    # send the info to root
    lets = comm.gather(list_of_executed_tasks, root=0)

    if worker_id == 0:
        # flatten the list of dicts into a single multilevel dict
        all_lets = {}
        for i in range(na):
            for step, item in lets[i].items():
                all_lets[step] = all_lets.get(step, {}) | item

        print('step     ', end='')
        for wid in range(na):
            print(f'{wid:4d} ', end='')
        print('\n' + '-'*(9 + (4 + 1)*na))
        for step in range(nt):
            print(f'{step:8d} ', end='')
            for wid in range(na):
                print(f'{all_lets[step][wid]:4d} ', end='')
            print()


def main(*, nt: int, step_time: float=0.015, ndata: int=10000):
    """
    Run a simulation

    :param nt: number of time steps
    """

    comm = MPI.COMM_WORLD
    worker_id = comm.Get_rank()
    num_workers = comm.Get_size()
    na = num_workers

    # create as many workers as there are age groups
    worker = Worker(na, nt, worker_id, ndata=ndata)

    # gather info about which tasks have been executed
    list_of_executed_tasks = {}

    tic = MPI.Wtime()

    #
    # iterate over the time steps
    # 
    for step in range(nt):

        # get the task ID (= cohort ID)
        tid = worker.get_task_to_execute()

        list_of_executed_tasks[step] = list_of_executed_tasks.get(step, {})

        # execute the task for this time step
        worker.execute_step(step_time=step_time)

        list_of_executed_tasks[step][worker_id] = tid

    toc = MPI.Wtime()

    print_info(list_of_executed_tasks, na, nt, comm, worker_id)

    if worker_id == 0:
        elapsed_time = toc - tic
        print(f'Elapsed time: {elapsed_time:.3f} secs')
        print(f'Speedup: {na*nt*step_time/elapsed_time:.3f}x (best case would be {num_workers})')


if __name__ == '__main__':
    defopt.run(main)

    
