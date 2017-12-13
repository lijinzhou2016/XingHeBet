import os
import sys
import time
import traceback
import json

import requests

from bet.settings import HttperConstant


class Httper(object):
    def __init__(self):
        self.__cookie_value = ""
        self.__cookie_key = HttperConstant.COOKIES_KEY

    def __format_post_url(self):
        return HttperConstant.BET_URL.format(str(round(time.time(), 3)).replace(".", ""))

    def __read_cookie_from_file(self):
        """读取本地文件获取cookies

        :return: cookies
        """
        try:
            if os.path.exists(HttperConstant.COOKIES_FILE_NAME):
                with open(HttperConstant.COOKIES_FILE_NAME, 'r') as f:
                    return f.read()
            else:
                return None
        except:
            traceback.print_exc()
            return None

    def __write_cookie_to_file(self, cookie):
        """保存cookies到本地文件

        :param cookies:
        :return:
        """
        try:
            with open(HttperConstant.COOKIES_FILE_NAME, 'w') as f:
                f.write(cookie)
            return True
        except:
            traceback.print_exc()
            return False

    def __input_cookie(self):
        return input(HttperConstant.INPUT_COOKIES_NOTE)

    def __get_headers(self):
        return {"Cookie": HttperConstant.COOKIES_KEY+"="+self.get_cookie()}

    def __load_cookie(self, local=False):
        if local:
            try:
                return self.__read_cookie_from_file()
            except:
                traceback.print_exc()
                return None
        else:
            return self.__input_cookie()

    def get_cookie(self):
        return self.__cookie_value

    def check_cookie(self):
        rs = self.post(self.__format_post_url(),
                       data={'betForm': json.dumps(HttperConstant.TEST_COOKIES_DATA)},
                       headers=self.__get_headers()
                       )
        if "login.html" in rs:
            return False
        else:
            return True

    def set_cookie(self, local=False):
        """设置 self.__cookies的值，并保存到.cookies文件中

        :param local: True: 从本地文件读取，False：输入cookies
        :return: 执行成功与否 True/False
        """
        cookie = self.__load_cookie(local=local)
        if cookie is None:
            return False
        else:
            self.__write_cookie_to_file(cookie)
            self.__cookie_value = cookie
            return self.check_cookie()

    def post(self, url, data=None, headers=None, timeout=5):
        if headers is None:
            headers = self.__get_headers()

        try:
            rs = requests.post(url, data=data, headers=headers, timeout=timeout)
            if rs.status_code == 200:
                print(rs.text)
                return rs.text
            else:
                return None
        except:
            traceback.print_exc()
            return None

    def get(self, url, timeout=5):
        try:
            rs = requests.get(url, timeout=timeout)
            if rs.status_code == 200:
                return rs.json()
            else:
                print('receive code: ' + str(rs.status_code))
                return None
        except Exception as e:
            print(str(e))
            return None


if __name__ == "__main__":
    httper = Httper()
    if not httper.set_cookie(local=True):
        if not httper.set_cookie():
            httper.set_cookie()

    post_data = {
        "code": "cqssc",
        "quantity": 1,
        "totalMoney": 2,
        "betOrders": [
            {
                "expect": "20171212100",
                "code": "cqssc",
                "betCode": "ten_thousand",
                "playCode": "one_big_small",
                "betNum": "大",
                "odd": "1.98",
                "betAmount": "1",
                "memo": ""
            }
        ]
    }

    rs = httper.post(HttperConstant.BET_URL, data={'betForm': json.dumps(post_data)})
    print(rs)