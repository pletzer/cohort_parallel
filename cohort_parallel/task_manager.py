import logging


class TaskManager:

    def __init__(self, na, nt, num_workers=1):
        """
        Constructor
        :param na: number of age groups
        :param nt: number of time steps
        """
        self.na = na
        self.nt = nt
        self.num_cohorts = na + nt - 1

        # initially
        self.worker2task = {wid: [] for wid in range(num_workers)}
        for i in range(na):
            worker_id = i % num_workers
            self.worker2task[worker_id].append(i)


    def get_init_task_ids(self, worker_id):
        """
        Get the initial task Ids for this worker, when the simulation starts
        :param worker_id: worker ID (range 0 to num procs - 1)
        """
        return self.worker2task[worker_id]

 
    def get_num_steps(self, task_id):
        """
        Get the number of time steps of the current task
        :param task_id: task ID
        :returns number
        """
        # if task_id < self.na
        res = self.na - task_id
        if self.na <= task_id < self.nt:
            res = self.na
        elif task_id >= self.nt:
            res = self.na + self.nt - task_id - 1
        return res


    def get_initial_dependencies(self, task_id):
        """
        Get all the task dependencies for the current task
        :param task_id: task ID
        :returns number
        """
        res = None
        if task_id > 2*self.na - 1:
            res = {i for i in range(task_id - self.na + 1, task_id)}
        elif self.na <= task_id <= 2*self.na - 1:
            res = {i for i in range(2*self.na - 1 - task_id)}.union({i for i in range(self.na, task_id)})
        return res


    def get_next_task(self, task_id):
        """
        Get the following task ID
        :param task_id: task ID
        :returns number or None if this is the last task to be executed
        """
        res = task_id + self.na
        if task_id < self.na:
            res = task_id + 2*(self.na - 1 - task_id) + 1
        elif task_id >= self.nt - 1:
            # last task
            res = None
        return res



