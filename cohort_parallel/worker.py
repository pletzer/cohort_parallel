import time
from task_manager import TaskManager


class Worker:

    def __init__(self, na, nt, worker_id):
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


    def get_num_time_steps_to_execute(self):
        """
        Get the number of time steps to execute in the queued task
        :returns number
        """
        return self.task.get_num_time_steps(self.task_id)


    def execute_task(self, exec_sec=1):
        """
        Execute the task
        :param exec_sec: time it takes to execute one time step in secs
        :returns the next task ID or None if there are no more tasks
        """
        nsteps = self.task.get_num_time_steps(self.task_id)
        # zzzzzzz....
        time.sleep(nsteps * exec_sec)
        self.task_id = self.task.get_next_task(self.task_id)
        return self.task_id


    def get_task_to_execute(self):
        """
        Get the task ID in the queue
        :returns number
        """
        return self.task_id


