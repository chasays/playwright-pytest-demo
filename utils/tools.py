import base64
import time
import os
import requests
import json
import random
from globaldata.data import G
from faker import Faker
from PIL import Image, ImageDraw


def decode_base64(b):
    return base64.b64decode(b).decode('utf-8')


def generate_random_str():
    # str(uuid.uuid4()).replace('-', '').upper()
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())


def random_int(max=99999):
    return random.randint(0, max)


def random_str(max=9999):
    return str(random_int(max))


def get_tmp_url():
    session = requests.session()
    cookies = getcookies_decode_to_dict()
    session.cookies.update(cookies)
    ret = session.post('xxxxx', data={'surveyId': xxx})
    session.get(url='http://xx.xx.com')
    return ret.text  # cookies too large


def getcookies_decode_to_dict():
    cookies_dict = {}
    with open(G.STATE_JSON, 'rb') as f:
        content = json.loads(f.read())
        cookies = content.get('cookies')
        origins = content.get('origins')[0]['localStorage']  # origins[0]['localStorage']
        if cookies:
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
        if origins:
            for cookie in origins:
                cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict


def generate_any(type='text'):
    # 根据type的值 text/name/address，自动生成对应的text
    fake = Faker('zh_CN')
    cmd = f'fake.{type}()'
    return eval(cmd)


def generate_pic():
    img = Image.new('RGB', (300, 300), color=(random_int(255), random_int(255), random_int(255)))
    d = ImageDraw.Draw(img)
    d.text((10, 10), generate_random_str(), spacing=10, fill=(random_int(255), random_int(255), random_int(255)))
    img.save(G.TMP_PIC_PATH)


if __name__ == '__main__':
    # print(generate_any('address'))
    generate_pic()
