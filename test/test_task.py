import unittest
import datetime
from api.task import Task


class TaskParse(unittest.TestCase):
    """
    测试单个task相关
    """

    def test_create_from_str_1(self):
        task = Task("x (A) 2016-05-20 2016-04-30 measure space for +chapelShelving @chapel due:2016-05-30")
        # task.show()
        self.assertTrue(task.is_completed)
        self.assertIs(task.priority, 'A')
        self.assertIn(task.description, "measure space for +chapelShelving @chapel due:2016-05-30")
        self.assertIs(len(task.description), len('measure space for +chapelShelving @chapel due:2016-05-30'))
        self.assertIn('chapelShelving', task.tag["project"])
        self.assertIn('chapel', task.tag["context"])

    def test_create_from_str_2(self):
        task = Task("(A) 2022-04-23 read <<Python Crash Course>> @read @code +work author:Eric")
        # task.show()
        self.assertFalse(task.is_completed)
        self.assertIs(task.priority, 'A')
        self.assertIn(task.description, "read <<Python Crash Course>> @read @code +work author:Eric")
        self.assertIn('work', task.tag["project"])
        self.assertIn('read', task.tag["context"])
        self.assertIn('code', task.tag["context"])

    def test_add_tag(self):
        task = Task("cook")
        task.add_tag("project", "dinner")
        self.assertIn('dinner', task.tag["project"])

    def test_del_tag(self):
        task = Task("cook")
        task.add_tag("project", "dinner")
        task.remove_tag("project", "dinner")
        self.assertNotIn('dinner', task.tag["project"])

    def test_modify_tag(self):
        task = Task("cook")
        task.add_tag("project", "dinner")
        task.replace_tag("project", "dinner", "breakfast")
        self.assertIn('breakfast', task.tag["project"])
        self.assertNotIn('dinner', task.tag["project"])

    def test_set_status(self):
        task = Task("cook")
        self.assertFalse(task.is_completed)
        task.set_completed_status(True)
        self.assertTrue(task.is_completed)

    def test_set_priority(self):
        task = Task("cook")
        task.set_priority('A')
        self.assertIs('A', task.priority)


if __name__ == '__main__':
    unittest.main()
