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


def _trans_time(date):
    match = DATE_RE.match(date)
    if match:
        return datetime.datetime.strptime(date, DATE_FMT).date()
    else:
        return None  # not a datetime like"xxxx-xx-xx"


class Task:
    """
        负责单条task的类
    """

    def __init__(self, str_raw=None):
        """
        初始化task，无参数则新建空task
        :param str_raw: (str) 原始字符串
        """
        self.raw = None                 # 原始字符串
        self.is_completed = False       # 是否done标记
        self.priority = None            # 优先级
        self.completion_date = None     # 完成日期
        self.creation_date = None       # 创建日期
        self.description = ""           # task描述
        self.tag = {"project": [], "context": []}           # project和context标签
        self.metadata = {}              # 元数据
        self._raw_list = []             # 原始字符串用空格分割得到的列表
        self._description_list = []     # task描述部分用空格分割的列表

        self.tag_sign = {"project": '+', "context": '@'}            # tag的类型和描述符对应表
        self.tag_sign_reverse = {'+': "project", '@': "context"}    # tag的类型和描述符反对应表

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
        raw = raw.strip()
        raw_list = raw.split()
        self._raw_list = raw_list[:]
        self._parse_list(raw_list)

    def _parse_list(self, raw_list):
        """
        从list构建task
        :param raw_list: 将原始字符串用空格分割得到的list
        :return:
        """
        # 是否完成标记
        if raw_list[0] == 'x':
            self.set_completed_status(True)
            del raw_list[0]
        else:
            self.set_completed_status(False)

        # 优先级
        if PRIORITY_RE.match(raw_list[0]):
            self.set_priority(raw_list[0][1])
            del raw_list[0]

        # 完成时间
        if self.is_completed and self.set_completion_time(raw_list[0]):
            del raw_list[0]

        # 创建时间
        if self.set_creation_time(raw_list[0]):
            del raw_list[0]

        # 主体部分的处理
        self._parse_description(raw_list)

    def _parse_description(self, description_list):
        """
        处理Description部分
        :param description_list: 主体部分的list
        :return:
        """
        self.empty_description()
        self._description_list = description_list[:]
        for word in description_list:
            self.description += word + " "
            if self.add_tag(word):
                self._description_list.pop()
            if self.add_metadata(word):
                self._description_list.pop()
        self.description = self.description.strip()

    def set_completed_status(self, status):
        """
        设置task状态，当前仅True和False两种，即完成和未完成
        :param status: (bool) 完成状态
        :return:
        """
        self.is_completed = status

    def set_priority(self, priority=None):
        """
        设置优先级 无参数时为删除优先级
        :param priority: (str) 优先级[A-Z]
        :return:
        """
        if priority is None:
            self.priority = priority
            return True
        elif priority.isalpha() and len(priority) == 1:
            self.priority = priority.upper()
            return True
        else:
            return False  # not a upper alpha

    def set_creation_time(self, date_str):
        """
        设置创建时间
        :param date_str: (str) 时间
        :return:
        """
        date = _trans_time(date_str)
        if date:
            self.creation_date = date
            return True
        else:
            return False

    def set_completion_time(self, date_str):
        """
        设置完成时间
        :param date_str: (str) 时间
        :return:
        """
        date = _trans_time(date_str)
        if date:
            self.completion_date = date
            return True
        else:
            return False

    def add_tag(self, tag):
        """
        增加标签，如project、context等
        :param tag: (str) 标签名 带有+或者@的描述符号
        :return:
        """
        if tag[0] in list(self.tag_sign_reverse.keys()):
            tag_type = self.tag_sign_reverse[tag[0]]
            self.tag[tag_type].append(tag)
            self._description_list.append(tag)
            return True
        else:
            return False

    def remove_tag(self, tag):
        """
        删除标签，指定类型和标签名
        :param tag: (str) 带标签名 带有+或者@的描述符号
        :return:
        """
        if tag[0] in list(self.tag_sign_reverse.keys()):
            tag_type = self.tag_sign_reverse[tag[0]]
            self.tag[tag_type].remove(tag)
        self._description_list.remove(tag)

    def replace_tag(self, old, new):
        """
        修改tag
        :param old: (str) 原标签名 带有+或者@的描述符号
        :param new: (str) 新标签名 带有+或者@的描述符号
        :return:
        """
        tag_type = self.tag_sign_reverse[old[0]]
        if old in self._description_list and old in self.tag[tag_type]:
            index_des = self._description_list.index(old)
            index_tag = self.tag[tag_type].index(old)
            self._description_list[index_des] = new
            self.tag[tag_type][index_tag] = new
            return True
        else:
            return False  # tag is not in _description_list or tag list

    def replace_description(self, description):
        """
        修改主体内容，会同时修改tag
        :param description:
        :return:
        """
        self.description = ''
        self.append_description(description)

    def append_description(self, append_words):
        """
        description追加内容
        :param append_words: (str) 追加的内容
        """
        append_words = append_words.strip()
        self.description += ' ' + append_words
        new_list = self.description.split()
        self._parse_description(new_list)

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
                self._description_list.append(metadata)
                return True
            return False
        else:
            return False # not a metadata

    def replace_metadata(self, metadata):
        return self.add_metadata(metadata)

    def remove_metadata(self, metadata_key):
        """
        删除元数据
        :param metadata_key:
        :return:
        """
        if metadata_key in self.metadata.keys():
            del self.metadata[metadata_key]
            return True
        else:
            return False

    def restruct_raw_list(self):
        self._raw_list.clear()

        if self.is_completed:
            self._raw_list.append('x')

        if self.priority:
            self._raw_list.append(f"({self.priority})")

        if self.completion_date:
            self._raw_list.append(self.completion_date.strftime(DATE_FMT))

        if self.creation_date:
            self._raw_list.append(self.creation_date.strftime(DATE_FMT))

        for word in self._description_list:
            self._raw_list.append(word)

    def get_description(self):
        return ' '.join(self._description_list)

    def empty_description(self):
        """
        清空task的description
        """
        self.description = ""  # task描述
        self.tag = {"project": [], "context": []}  # project和context标签
        self.metadata = {}  # 元数据
        self._raw_list = []  # 原始字符串用空格分割得到的列表
        self._description_list = []  # task描述部分用空格分割的列表

    def __str__(self):
        self.restruct_raw_list()
        return ' '.join(self._raw_list)

    def show(self):
        print(f"Priority: {self.priority}")
        print(f"Completed: {self.is_completed}")
        print(f"Creation: {self.creation_date}")
        print(f"Completion: {self.completion_date}")
        print(f"Description: {self.description}")
        print(f"tag: {self.tag}")
        print(f"meta: {self.metadata}")

