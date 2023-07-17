from mpi4py import MPI
import defopt
from worker import Worker

import sys
import logging
logging.basicConfig(format='%(asctime)s: %(message)s') #, level=logging.DEBUG)

def main(*, nt: int):
    """
    Run a simulation

    :param nt: number of time steps
    """
    comm = MPI.COMM_WORLD
    worker_id = comm.Get_rank()
    num_workers = comm.Get_size()
    na = num_workers

    worker = Worker(na, nt, worker_id)

    # gather info about tasks are being executed
    list_of_executed_tasks = {}

    #
    # iterate over the time steps
    # 
    for step in range(nt):
        tid = worker.get_task_to_execute()
        list_of_executed_tasks[step] = list_of_executed_tasks.get(step, {})

        # execute the task
        worker.execute_step()

        list_of_executed_tasks[step][worker_id] = tid

    #
    # print the info
    #

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

if __name__ == '__main__':
    defopt.run(main)

    