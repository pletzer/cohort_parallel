from cohort_parallel import task

def test_task4_5():
	t = Task(4, 8)
	assert(t.get_num_tasks() == 11)
	assert(t.num_num_time_steps(0) == 4)
	assert(t.get_num_time_steps(1) == 3)
	assert(t.get_num_time_steps(2) == 2)
	assert(t.get_num_time_steps(3) == 1)
	assert(t.get_num_time_steps(4) == 4)
	assert(t.get_num_time_steps(5) == 4)
	assert(t.get_num_time_steps(6) == 4)
	assert(t.get_num_time_steps(7) == 4)
	assert(t.get_num_time_steps(8) == 3)
	assert(t.get_num_time_steps(9) == 2)
	assert(t.get_num_time_steps(10) == 1)