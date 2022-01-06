# @Time : 2021/4/18 
# @Author : xiaorik
import json
from globaldata.data import G
from utils.tools import decode_base64


class User(object):

    def __init__(self, username=None, password=None, desc=None):
        self.username = username
        self.password = password
        self.desc = desc

    def __str__(self):
        return json.dumps(self.__dict__)


def test_user():
    username = 'test_1' # todo
    password = 'test_1'
    return User(username=username, password=password, desc='this is normal')


def test_admin_user():
    username = 'admin1'
    password = 'admin1'
    return User(username=username, password=password, desc='this is a admin user')


def product_user():
    username = G.USERNAME
    password = G.PASSWORD
    return User(username=decode_base64(username), password=decode_base64(password), desc='this is a product user')


def login_user():
    if 'test' in G.CUR_ENV:
        return test_user()
    else:
        return product_user()
