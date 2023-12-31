from cohort_parallel import TaskManager


def test_task2_3():
    """
    0 1
    2 0
    3 2
    """
    t = TaskManager(na=2, nt=3, num_workers=1)

    assert(t.get_num_steps(0) == 2)
    assert(t.get_num_steps(1) == 1)
    assert(t.get_num_steps(2) == 2)
    assert(t.get_num_steps(3) == 1)

    assert(t.get_initial_dependencies(0) is None)
    assert(t.get_initial_dependencies(1) is None)
    assert(t.get_initial_dependencies(2) == {0})
    assert(t.get_initial_dependencies(3) == {2})

    assert(t.get_next_task(0) == 3)
    assert(t.get_next_task(1) == 2)
    assert(t.get_next_task(2) == None)
    assert(t.get_next_task(3) == None)


def test_task3_10():
    """
     0  1  2
     3  0  1
     4  3  0
     5  4  3
     6  5  4
     7  6  5
     8  7  6
     9  8  7
    10  9  8
    11 10  9
    """
    t = TaskManager(na=3, nt=10)

    assert(t.get_num_steps(0) == 3)
    assert(t.get_num_steps(1) == 2)
    assert(t.get_num_steps(2) == 1)
    assert(t.get_num_steps(3) == 3)
    assert(t.get_num_steps(4) == 3)
    assert(t.get_num_steps(5) == 3)
    assert(t.get_num_steps(6) == 3)
    assert(t.get_num_steps(7) == 3)
    assert(t.get_num_steps(8) == 3)
    assert(t.get_num_steps(9) == 3)
    assert(t.get_num_steps(10) == 2)
    assert(t.get_num_steps(11) == 1)

    assert(t.get_initial_dependencies(0) is None)
    assert(t.get_initial_dependencies(1) is None)
    assert(t.get_initial_dependencies(2) is None)
    assert(t.get_initial_dependencies(3) == {0, 1})
    assert(t.get_initial_dependencies(4) == {3, 0})
    assert(t.get_initial_dependencies(5) == {4, 3})
    assert(t.get_initial_dependencies(6) == {5, 4})
    assert(t.get_initial_dependencies(7) == {6, 5})
    assert(t.get_initial_dependencies(8) == {7, 6})
    assert(t.get_initial_dependencies(9) == {8, 7})
    assert(t.get_initial_dependencies(10) == {9, 8})
    assert(t.get_initial_dependencies(11) == {10, 9})

    assert(t.get_next_task(0) == 5)
    assert(t.get_next_task(1) == 4)
    assert(t.get_next_task(2) == 3)
    assert(t.get_next_task(3) == 6)
    assert(t.get_next_task(4) == 7)
    assert(t.get_next_task(5) == 8)
    assert(t.get_next_task(6) == 9)
    assert(t.get_next_task(7) == 10)
    assert(t.get_next_task(8) == 11)
    assert(t.get_next_task(9) == None)
    assert(t.get_next_task(10) == None)
    assert(t.get_next_task(11) == None)


def test_task4_8():
    """
     0  1  2  3
     4  0  1  2
     5  4  0  1
     6  5  4  0
     7  6  5  4
     8  7  6  5
     9  8  7  6
    10  9  8  7
    """
    t = TaskManager(4, 8)

    assert(t.get_num_steps(0) == 4)
    assert(t.get_num_steps(1) == 3)
    assert(t.get_num_steps(2) == 2)
    assert(t.get_num_steps(3) == 1)
    assert(t.get_num_steps(4) == 4)
    assert(t.get_num_steps(5) == 4)
    assert(t.get_num_steps(6) == 4)
    assert(t.get_num_steps(7) == 4)
    assert(t.get_num_steps(8) == 3)
    assert(t.get_num_steps(9) == 2)
    assert(t.get_num_steps(10) == 1)

    assert(t.get_initial_dependencies(0) is None)
    assert(t.get_initial_dependencies(1) is None)
    assert(t.get_initial_dependencies(2) is None)
    assert(t.get_initial_dependencies(3) is None)
    assert(t.get_initial_dependencies(4) == {0, 1, 2})
    assert(t.get_initial_dependencies(5) == {4, 0, 1})
    assert(t.get_initial_dependencies(6) == {5, 4, 0})
    assert(t.get_initial_dependencies(7) == {6, 5, 4})
    assert(t.get_initial_dependencies(8) == {7, 6, 5})
    assert(t.get_initial_dependencies(9) == {8, 7, 6})
    assert(t.get_initial_dependencies(10) == {9, 8, 7})

    assert(t.get_next_task(0) == 7)
    assert(t.get_next_task(1) == 6)
    assert(t.get_next_task(2) == 5)
    assert(t.get_next_task(3) == 4)
    assert(t.get_next_task(4) == 8)
    assert(t.get_next_task(5) == 9)
    assert(t.get_next_task(6) == 10)
    assert(t.get_next_task(7) == None)
    assert(t.get_next_task(8) == None)
    assert(t.get_next_task(9) == None)
    assert(t.get_next_task(10) == None)

   

if __name__ == '__main__':
    test_task2_3()
    test_task3_10()
    test_task4_8()