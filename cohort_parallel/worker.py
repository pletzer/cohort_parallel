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

        # time to execute one step
        self.one_step_time = 1


    def get_num_time_steps_to_execute(self):
        return self.task.get_num_time_steps(self.task_id)


    def execute_task(self):
        nsteps = self.task.get_num_time_steps(self.task_id)
        time.sleep(nsteps * self.one_step_time)
        self.task_id = self.task.get_next_task(self.task_id)
        return self.task_id


    def get_task_to_execute(self):
        return self.task_id


