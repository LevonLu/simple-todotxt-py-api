import datetime
import re

COMPLETED_RE = re.compile(r'^x\s+')
PRIORITY_RE = re.compile(r'\(([A-Z]+)\)')
PROJECT_RE = re.compile(r'\+([^\s]+)')
CONTEXT_RE = re.compile(r'@([^\s]+)')
KEYVALUE_RE = re.compile(r'([^\s]+):([^\s$]+)')
DATE_RE = re.compile(r'^\s*([\d]{4}-[\d]{2}-[\d]{2})', re.ASCII)
DATE_FMT = '%Y-%m-%d'
KEYVALUE_ALLOW = set(['http', 'https', 'mailto', 'ssh', 'ftp'])


class Task:
    """
        负责单条task的类
    """

    def __init__(self, str_raw=None):
        """
        初始化task，无参数则新建空task
        :param str_raw: (str) 原始字符串
        """
        self.raw = None
        self.is_completed = False
        self.priority = None
        self.completion_date = None
        self.creation_date = None
        self.main_body = ""
        self.tag = {"project": [], "context": []}
        self.metadata = {}
        self._raw_list = []

        if str_raw:
            self.raw = str_raw
            self.parse_str(str_raw)
        else:
            pass

    def parse_str(self, raw):
        """
        从字符串解析task
        :param raw: (str) 原始字符串
        :return:
        """
        raw.strip()
        self.parse_list(raw.split())

    def parse_list(self, raw_list):
        """
        从list构建task
        :param raw_list: 将原始字符串用空格分割得到的list
        :return:
        """
        # 是否完成标记
        if raw_list[0] == 'x':
            self.is_completed = True
            del raw_list[0]
        else:
            self.is_completed = False

        # 优先级
        match_priority = PRIORITY_RE.match(raw_list[0])
        if match_priority:
            self.priority = raw_list[0][1]
            del raw_list[0]

        # 完成日期
        match_completion_date = DATE_RE.match(raw_list[0])
        if match_completion_date is not None:
            self.completion_date = datetime.datetime.strptime(raw_list[0], DATE_FMT).date()
            del raw_list[0]

        # 创建日期
        match_creation_date = DATE_RE.match(raw_list[0])
        if match_creation_date is not None:
            self.creation_date = datetime.datetime.strptime(raw_list[0], DATE_FMT).date()
            del raw_list[0]

        # 主体部分的处理
        self.parse_main_body(raw_list)

    def parse_main_body(self, raw_list):
        """
        处理Description部分
        :param raw_list: 主体部分的list
        :return:
        """
        for word in raw_list:
            self.main_body += word + " "
            match_project = PROJECT_RE.match(word)
            match_context = CONTEXT_RE.match(word)
            match_meta = KEYVALUE_RE.match(word)
            if match_context:
                self.tag["context"].append(word[1:])
            elif match_project:
                self.tag["project"].append(word[1:])
            elif match_meta:
                key_value = word.split(':')
                if key_value[0] not in KEYVALUE_ALLOW:
                    self.metadata[key_value[0]] = key_value[1]
            else:
                pass
        self.main_body = self.main_body.strip()

    def add_tag(self, item, tag):
        """
        增加标签，如project、context等
        :param item: (str) 标签类型
        :param tag: (str) 标签名
        :return:
        """
        self.tag[item].append(tag)

    def del_tag(self, item, tag):
        """
        删除标签，指定类型和标签名
        :param item: (str) 标签类型
        :param tag: (str) 标签名
        :return:
        """
        self.tag[item].remove(tag)

    def modify_tag(self, item, old, new):
        """
        修改tag
        :param item: (str) 标签类型
        :param old: (str) 原标签名
        :param new: (str) 新标签名
        :return:
        """
        self.del_tag(item, old)
        self.add_tag(item, new)

    def set_completed_status(self, status):
        """
        设置task状态，当前仅True和False两种，即完成和未完成
        :param status: (bool) 完成状态
        :return:
        """
        self.is_completed = status

    def set_priority(self, priority):
        """
        设置优先级
        :param priority: (str) 优先级[A-Z]
        :return:
        """
        if priority.isalpha() and len(priority) == 1:
            self.priority = priority.upper()
        else:
            pass  # not a upper alpha

    def set_creation_time(self, date):
        """
        设置创建时间
        :param date: (str) 时间
        :return:
        """
        match = DATE_RE.match(date)
        if match:
            self.creation_date = datetime.datetime.strptime(date, DATE_FMT).date()
        else:
            pass  # not a datetime like"xxxx-xx-xx"

    def set_completion_time(self, date):
        """
        设置完成时间
        :param date: (str) 时间
        :return:
        """
        match = DATE_RE.match(date)
        if match:
            self.completion_date = datetime.datetime.strptime(date, DATE_FMT).date()
        else:
            pass  # not a datetime like"xxxx-xx-xx"

    def modify_main_body(self, main):
        """
        修改主体内容，会一起修改project和context
        :param main:
        :return:
        """
        self.tag["project"].clear()
        self.tag["context"].clear()
        self.metadata.clear()
        self.main_body = ""

        self.parse_main_body(main.split())

    def add_metadata(self, metadata):
        """
        增加元数据
        :param metadata:
        :return:
        """
        match_meta = KEYVALUE_RE.match(metadata)
        if match_meta:
            key_value = metadata.split(':')
            if key_value[0] not in KEYVALUE_ALLOW:
                self.metadata[key_value[0]] = key_value[1]
        else:
            pass  # not a metadata

    def modify_metadata(self, metadata):
        self.add_metadata(metadata)

    def del_metadata(self, metadata_key):
        """
        删除元数据
        :param metadata_key:
        :return:
        """
        del self.metadata[metadata_key]

    def show(self):
        print(f"Priority: {self.priority}")
        print(f"Completed: {self.is_completed}")
        print(f"Creation: {self.creation_date}")
        print(f"Completion: {self.completion_date}")
        print(f"Main body: {self.main_body}")
        print(f"tag: {self.tag}")
        print(f"meta: {self.metadata}")
