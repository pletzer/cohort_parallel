import time
import numpy as np
import logging
import numpy as np

class Task:

    def __init__(self, task_id, ndata=10000):
        """
        Constructor
        :param task_id: task ID in the range 0... na - 1
        :param ndata: number of doubles to accumulate at the end of each time step
        """
        self.task_id = task_id
        self.local_step = 0
        self.data = task_id * np.ones((ndata,), np.float64)


    def get_data(self):
        """
        Get the data associated with this task
        :returns array
        """
        return self.data


    def get_local_step(self):
        """
        Get the step in the task to execute
        :returns number
        """
        return self.local_step


    def get_task_id(self):
        """
        Get this task's ID
        :returns ID
        """
        return self.task_id


    def execute_step(self, step_time):
        """
        Execute one step
        :param exec_sec: time it takes to execute one time step in secs
        """

        #logging.debug(f'executing task {self.task_id} at local time step {self.local_step}...')

        # zzzzzzz.... simulates the code advancing by one time step
        time.sleep(step_time)

        # update the data
        self.data += 1

        # update the time step
        self.local_step += 1

        #logging.debug(f'{self.task_id} is done!')




