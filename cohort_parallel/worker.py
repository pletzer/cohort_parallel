import time
from task_manager import TaskManager
from mpi4py import MPI
from mpi4py.util import dtlib
import numpy as np
import logging

class Worker:

    def __init__(self, na, nt, worker_id, ndata=10000, comm=MPI.COMM_WORLD):
        """
        Constructor
        :param na: number of age groups
        :param nt: number of time steps
        :param worker_id: worker ID
        :param ndata: number of doubles each worker needs to share
        :param comm: MPI communicator
        """
        self.na = na
        self.nt = nt
        self.task = TaskManager(na, nt)

        self.worker_id = worker_id

        # initially only
        self.task_id = worker_id

        self.comm = comm
        self.proc_id = comm.Get_rank()

        self.step = 0

        self.srcBuffer = (-1) * np.ones((ndata,), np.float64)
        self.oldSrcBuffer = np.empty_like(self.srcBuffer)

        # allocate memory to receive the data from other workers
        self.rcvBuffer = np.empty((ndata,), np.float64)
        self.rcvWindow = MPI.Win.Create(self.rcvBuffer, comm=comm)


    def __del__(self):
    	"""
    	Destructor
    	"""
    	self.rcvWindow.Free()


    def get_id(self):
        """
        Get this worker's ID
        :returns number
        """
        return self.worker_id


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


    def execute_step(self, step_time):
        """
        Execute one step of a task (task = cohort)
        :param exec_sec: time it takes to execute one time step in secs
        """

        logging.debug(f'worker {self.proc_id} is executing task {self.task_id}...')

        # zzzzzzz.... simulates the code advancing by one time step
        time.sleep(step_time)

        logging.debug(f'worker {self.proc_id} is done!')

        # copy, we will need to remove this contribution from the summed data
        self.oldSrcBuffer[:] = self.srcBuffer

        # update the data to share with other workers
        self.srcBuffer[:] += 1.0

        ns = self.task.get_num_time_steps(self.task_id)

        # update the time step
        self.step += 1

        # at this point the data to get from the the cohorts are ready
        # we're telling that the window operation is the first and will not involve RMA puts
        self.rcvWindow.Fence(MPI.MODE_NOPUT | MPI.MODE_NOPRECEDE)

        if self.step >= ns:

        	# the worker run through all the time steps for this cohort
        	# we now need to get initial conditions from the other workers

            # reset
            self.task_id = self.task.get_next_task(self.task_id)

            # self.task_id is None if there are no more tasks to execute
            if self.task_id:

                self.step = 0

               	# sum the data from the other workers (including itself)
                self.rcvWindow.Accumulate(self.srcBuffer, target_rank=self.proc_id, op=MPI.SUM)

                # remove the contribution from itself
                self.rcvBuffer -= self.oldSrcBuffer
        
        # self.recvBuffer will be ready after this call
        self.rcvWindow.Fence(MPI.MODE_NOSUCCEED)

        # apply some operations on the received data
        #...


    def get_task_to_execute(self):
        """
        Get the task ID in the queue
        :returns number
        """
        return self.task_id


