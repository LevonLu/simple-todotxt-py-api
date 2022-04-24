import unittest
import datetime

import api.task
from api.task import Task


class TaskParse(unittest.TestCase):
    """
    测试单个task相关
    """

    def test_create_from_str_1(self):
        task = Task("x (A) 2016-05-20 2016-04-30 measure space for +chapelShelving @chapel due:2016-05-30")
        self.assertTrue(task.is_completed)
        self.assertEqual(task.priority, 'A')
        self.assertEqual(datetime.datetime.strptime('2016-05-20', api.task.DATE_FMT).date(), task.completion_date)
        self.assertEqual(datetime.datetime.strptime('2016-04-30', api.task.DATE_FMT).date(), task.creation_date)
        self.assertEqual("measure space for +chapelShelving @chapel due:2016-05-30", task.description)
        self.assertIn('+chapelShelving', task.tag["project"])
        self.assertIn('@chapel', task.tag["context"])
        self.assertEqual('2016-05-30', task.metadata.pop('due'))

    def test_create_from_str_2(self):
        task = Task("(A) 2022-04-23 read <<Python Crash Course>> @read @code +work author:Eric")
        self.assertFalse(task.is_completed)
        self.assertEqual(task.priority, 'A')
        self.assertEqual(datetime.datetime.strptime('2022-04-23', api.task.DATE_FMT).date(), task.completion_date)
        self.assertIn(task.description, "read <<Python Crash Course>> @read @code +work author:Eric")
        self.assertIn('+work', task.tag["project"])
        self.assertIn('@read', task.tag["context"])
        self.assertIn('@code', task.tag["context"])
        self.assertEqual('Eric', task.metadata.pop('author'))

    def test_tag_manipulate(self):
        task = Task("cook noodles")

        # add tag
        task.add_tag("+dinner")
        self.assertIn('+dinner', task.tag["project"])

        # replace tag
        task.replace_tag("+dinner", "+breakfast")
        self.assertIn('+breakfast', task.tag["project"])
        self.assertNotIn('+dinner', task.tag["project"])

        # del tag
        task.remove_tag('+breakfast')
        self.assertNotIn('+breakfast', task.tag["project"])

    def test_set_status(self):
        task = Task("cook")
        self.assertFalse(task.is_completed)
        task.set_completed_status(True)
        self.assertTrue(task.is_completed)

    def test_set_priority(self):
        task = Task("cook")
        task.set_priority('A')
        self.assertEqual('A', task.priority)

        task.set_priority()
        self.assertNotEqual('A', task.priority)


if __name__ == '__main__':
    unittest.main()
