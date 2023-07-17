from mpi4py import MPI
import defopt
from worker import Worker
from functools import reduce
import logging
logging.basicConfig(format='%(astime)s: %(message)%')


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
    
    # iterate over the time steps, gathering info about the time step, the worker id and the task id
    list_of_executed_tasks = {}
    for step in range(nt):
        tid = worker.get_task_to_execute()
        list_of_executed_tasks[step] = list_of_executed_tasks.get(step, {})
        worker.execute_step()
        list_of_executed_tasks[step][worker_id] = tid

    # send the info to root
    lets = comm.gather(list_of_executed_tasks, root=0)

    if worker_id == 0:

        # print the info

        # flatten the list of dicts into a single multilevel dict
        all_lets = {}
        for i in range(na):
            for step, item in lets[i].items():
                all_lets[step] = all_lets.get(step, {}) | item

        for it in range(nt):
            for wid in range(na):
                print(f'{all_lets[it][wid]:4d} ', end='')
            print()

if __name__ == '__main__':
    defopt.run(main)

    