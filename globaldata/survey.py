# @Time : 2021/6/18
# @Author : xiaorik
import json
from globaldata.data import G


class Survey(object):

    def __init__(self, id=None, code=None, type=None):
        """
        :param id: 问卷id
        :param code: 问卷short code/tracebackIdDec etc,.
        :param type: 问卷类型，普通问卷、防伪溯源、智能测款、第三方问卷等
        """
        self.id = id
        self.code = code
        self.type = type
        self.concat_url()

    def __str__(self):
        return json.dumps(self.__dict__)

    def concat_url(self):
        url = ''
        if 'trace' in self.type:
            url = 'https://answer.domainname.com/traceBack/page/detail?tracebackIdDec=' + self.code
        return url


def trace_back():
    # 返回 2 个 url，第一个为有效，第二个为无效
    if 'test' in G.CUR_ENV:
        return '123', '124' # todo
    elif 'pre' in G.CUR_ENV:
        return '123', '124'
    else:
        return '123', '124'


def answer_url():
    # G.ANSWER_URL 由test_all_next_and_submit用例生成，没有执行这个值为空
    if G.ANSWER_URL:
        return G.ANSWER_URL
    if 'test' in G.CUR_ENV:
        return '1' # todo
    elif 'pre' in G.CUR_ENV:
        return '2'
    else:
        return '3'


def answer_ic_url():
    # 工具survey_id获取临时预览链接
    if 'test' in G.CUR_ENV:
        return '2' # todo
    elif 'pre' in G.CUR_ENV:
        return '3'
    else:
        return '4'
