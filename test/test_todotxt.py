import unittest
import datetime
from api.todotxt import TodoTxt

DATE_FMT = '%Y-%m-%d'


class MyTestCase(unittest.TestCase):
    def test_init_from_file(self):
        todotxt = TodoTxt("todo.txt")
        ls = todotxt.get_task_list_str()
        self.assertIn('x (A) 2016-05-20 2016-04-30 measure space for +chapelShelving @chapel due:2016-05-30', ls)
        self.assertIn('cook noodles +dinner', ls)

    def test_task_manipulate(self):
        todotxt = TodoTxt("todo.txt")
        task_add = "shopping cola apple +shopping"

        # add task
        todotxt.add(task_add)
        ls = todotxt.get_task_list_str()
        task_add = datetime.datetime.now().strftime(DATE_FMT) + ' ' + task_add
        self.assertIn(task_add, ls)

        # task done
        todotxt.done(3)
        ls = todotxt.get_task_list_str()
        task_add = 'x ' + datetime.datetime.now().strftime(DATE_FMT) + ' ' + task_add
        self.assertIn(task_add, ls)

        todotxt.save('test_task_manipulate.txt')


if __name__ == '__main__':
    unittest.main()
