import time
from task_manager import TaskManager
from mpi4py import MPI
from mpi4py.util import dtlib
import numpy as np
import logging

class Worker:

    def __init__(self, na, nt, worker_id, comm=MPI.COMM_WORLD):
        """
        Constructor
        :param na: number of age groups
        :param nt: number of time steps
        :param worker_id: worker ID
        """
        self.na = na
        self.nt = nt
        self.task = TaskManager(na, nt)
        # initially
        self.task_id = worker_id
        self.comm = comm
        self.me = comm.Get_rank()

        self.step = 0

        ndata = 10
        self.srcBuffer = (-1) * np.ones((ndata,), np.float64)
        # attach the buffer to the MPI window
        self.window = MPI.Win.Create(self.srcBuffer, comm=comm)
        # allocate memory to receive the data from other workers
        self.rcvBuffer = np.empty((ndata,), np.float64)


    def get_num_time_steps_to_execute(self):
        """
        Get the number of time steps to execute for the queued task
        :returns number
        """
        return self.task.get_num_time_steps(self.task_id)


    def get_step(self):
        """
        Get the step in the task to execute
        :returns number
        """
        return self.step


    def execute_step(self, exec_sec=1):
        """
        Execute one step of a task (task = cohort)
        :param exec_sec: time it takes to execute one time step in secs
        """

        logging.debug(f'worker {self.me} is executing task {self.task_id}...')

        # zzzzzzz....
        time.sleep(exec_sec)

        logging.debug(f'worker {self.me} is done!')

        # update the data
        self.srcBuffer[:] += 1.0

        ns = self.task.get_num_time_steps(self.task_id)

        # update the time step
        self.step += 1

        # we're telling that the window operation is the first and will not involve RMA put
        self.window.Fence(MPI.MODE_NOPUT | MPI.MODE_NOPRECEDE)

        if self.step >= ns:

            # reset
            self.task_id = self.task.get_next_task(self.task_id)

            # self.task_id is None if there are no more tasks to execute
            if self.task_id:

                self.step = 0

                # fetch the data from the remote workers
                other_task_ids = self.task.get_initial_dependencies(self.task_id)
                for tid in other_task_ids:
                    wid = self.task.get_worker(tid)

                    # asynchrounous remote memory read
                    self.window.Get([self.rcvBuffer, MPI.DOUBLE], target_rank=wid)
                    logging.debug(f'worker {self.me} received {self.rcvBuffer.size * self.rcvBuffer.itemsize} bytes from worker {wid} (task {tid})')
        
        # closing window operation
        self.window.Fence(MPI.MODE_NOSUCCEED)
        # worker {self.me} is now guaranteed to have received the data
        self.comm.Barrier()



    def get_task_to_execute(self):
        """
        Get the task ID in the queue
        :returns number
        """
        return self.task_id


