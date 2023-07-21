from mpi4py import MPI
import defopt
from worker import Worker

import sys
import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)


def print_info(list_of_executed_tasks, na, nt, comm, worker_id, proc_id):

    print(f'[{comm.Get_rank()}] list_of_executed_tasks = {list_of_executed_tasks}')

    # send the info to root
    lets = comm.gather(list_of_executed_tasks, root=0)

    if proc_id == 0:

        print(f'lets = {lets}')

        # flatten the list of dicts into a single multilevel dict
        all_lets = {}
        for i in range(na):
            for step, item in lets[i].items():
                all_lets[step] = all_lets.get(step, {}) | item

        print(f'all_lets = {all_lets}')

        # step: {worker_id: task_id}

        print('step     ', end='')
        for wid in range(na):
            print(f'{wid:4d} ', end='')
        print('\n' + '-'*(9 + (4 + 1)*na))

        for step in range(nt):
            print(f'{step:8d} ', end='')
            for wid in range(na):
                print(f'*** step={step} wid={wid}')
                print(f'{all_lets[step][wid]:4d} ', end='')
            print()


def main(*, na: int, nt: int, step_time: float=0.015, ndata: int=10000):
    """
    Run a simulation

    :param na: number of age groups
    :param nt: number of time steps
    :param step_time: time it takes to execute one step for one age group
    :param ndata: number of doubles to exchange between a cohort pair
    """

    comm = MPI.COMM_WORLD
    proc_id = comm.Get_rank()
    num_procs = comm.Get_size()

    # number of workers is always equal to the number of age groups
    num_workers = na

    # the work ids associated with this process
    worker_ids = [wid for wid in range(num_workers) if wid % num_procs == proc_id]

    # create the workers for this processing element
    workers = [Worker(na=na, nt=nt, worker_id=wid, ndata=ndata) for wid in worker_ids]

    # gather info about which tasks have been executed
    list_of_executed_tasks = {}

    tic = MPI.Wtime()

    #
    # iterate over workers
    #
    for worker in workers:

        worker_id = worker.get_id()

        print(f'*** [{proc_id}] uses worker_id = {worker_id}')
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

    print_info(list_of_executed_tasks, na, nt, comm, worker_id, proc_id)

    if proc_id == 0:
        elapsed_time = toc - tic
        print(f'Elapsed time: {elapsed_time:.3f} secs')
        print(f'Speedup: {na*nt*step_time/elapsed_time:.3f}x (best case would be {num_workers})')


if __name__ == '__main__':
    defopt.run(main)

    
