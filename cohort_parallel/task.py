

class Task:

	def __init__(self, na, nt):
		"""
		Constructor
		:param na: number of age groups
		:param nt: number of time steps
		"""
		self.na = na
		self.nt = nt

	def get_num_tasks(self):
		return self.nt + self.na - 1

	def get_num_time_steps(self, task_id):
		# if task_id < self.na
		res = self.na - task_id
		if self.na <= task_id < self.nt:
			res = self.na
		elif task_id >= self.nt:
			res = self.na + self.nt - task_id - 1
		return res

	def get_initial_dependencies(self, task_id):
		res = None
		if task_id >= 2*self.na - 1:
			res = {i - 1 for i in range(task_id, self.na - 1)}
		elif self.na <= task_id < 2*self.na - 1:
			res = {i for i in range(task_id - self.na + 2)}
			res += {i for range(self.na, task_id)}
		return res




