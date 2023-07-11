

class TaskManager:

    def __init__(self, na, nt):
        """
        Constructor
        :param na: number of age groups
        :param nt: number of time steps
        """
        self.na = na
        self.nt = nt


    def get_num_tasks(self):
        """
        Get the number of tasks (or cohorts)
        :returns number
        """
        return self.nt + self.na - 1

 
    def get_num_time_steps(self, task_id):
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


    def get_worker(self, task_id):
        """
        Get the worker ID for this task
        :param task_id: task ID
        :returns number        
        """
        if task_id < self.na:
            return task_id
        else:
            return (self.na - 1 - task_id) % self.na



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
        elif task_id > self.get_num_tasks() - self.na - 1:
            # last task
            res = None
        return res




