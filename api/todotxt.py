from api.task import Task
import datetime

DATE_FMT = '%Y-%m-%d'

class TodoTxt:
    """
    管理todo.txt
    """

    def __init__(self, todo_file=None):
        self.filename = todo_file
        self.tag_dict = {"project": [], "context": []}

        self.todo_list = []

        if todo_file is not None:
            self.parse(todo_file)

    def parse(self, todo_file):
        try:
            with open(todo_file) as file_object:
                for line in file_object:
                    task = Task(line)
                    self.todo_list.append(task)
        except FileNotFoundError:
            print(FileNotFoundError)

    def add(self, task_str):
        task = Task(task_str)
        if not task.is_completed:
            now_date = datetime.datetime.now().strftime(DATE_FMT)
            task.set_creation_time(now_date)
        self.todo_list.append(task)

    def done(self, number=1):
        if 0 <= number <= len(self.todo_list):
            self.todo_list[number-1].set_completed_status(True)
            now_date = datetime.datetime.now().strftime(DATE_FMT)
            self.todo_list[number-1].set_completion_time(now_date)
            return True
        else:
            return False

    def save(self, path=None):
        if path is None:
            path = self.filename
        with open(path, 'w') as file_object:
            file_object.write(str(self))

    def get_task_list_str(self):
        result = []
        for task in self.todo_list:
            result.append(str(task))
        return result

    def __str__(self):
        result = ''
        for task in self.todo_list:
            result += str(task) + '\n'
        return result
