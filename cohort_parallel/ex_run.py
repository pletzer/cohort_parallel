from mpi4py import MPI
import defopt
from worker import Worker


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

	list_of_executed_tasks = []
	next_task = -1
	while next_task is not None:
		list_of_executed_tasks.append( (worker.get_task_to_execute(), worker.get_num_time_steps_to_execute()) )
		next_task = worker.execute_task()

	fmt = ''
	for t, m in list_of_executed_tasks:
		fmt += f'{t}x{m} '
	print(f'worker {worker_id} executed tasks {fmt}')

if __name__ == '__main__':
	defopt.run(main)

	