import json
import os
import time
import traceback

import requests

from settings import HttperConstant

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re

from settings import BetsConstant
from common import get_login_time_stamp
from settings import conf
from yudama3 import get_captcha


def auto_login():
    index_url = "https://vs5566.net/"
    login_url = "https://www.vs5566.net/passport/login.html?t={0}"
    captcha = ""
    captcha_flag=False


    try:
        rs = requests.get(index_url, timeout=60)
        if rs.status_code == 200:
            lines = rs.text.split("\n")
            for line in lines:

                if '<img class="_vr_captcha_code" data-code="loginTop" src="/pcenter/captcha/loginTop.html?t=' in line:
                    print(line)
                    captcha_flag = True
                    api = line.replace('<img class="_vr_captcha_code" data-code="loginTop" src="',"").replace('"', "").strip()
                    url = index_url + api
                    rs = requests.get(url, timeout=60)
                    if rs.status_code == 200:
                        with open("loginTop.jpeg", 'wb') as f:
                            f.write(rs.content)
                if '<div class="form-group form-group-sm scode _vr_captcha_box" style="display: none">' in line:
                    # print("不需要验证码")
                    break

    except Exception as e:
        traceback.print_exc()
        time.sleep(5)
        exit(-1)

    if captcha_flag:
        captcha = get_captcha(conf['yundama_user'], conf['yundama_pwd'])
        print("验证码：" + captcha)

    post_url = login_url.format(get_login_time_stamp())
    headers = {
        "Soul-Requested-With":"XMLHttpRequest"
    }

    post_data = {
            "type": "top",
            "username": conf['xinghe_user'],
            "password": conf['xinghe_pwd'],
            "captcha": captcha
        }
    # print(post_data)
    # print(post_url)

    try:
        rs = requests.post(post_url, data=post_data, headers=headers, timeout=60)
        if rs.status_code == 200:
            if rs.json().get("success"):
                print(u"=== 登录星河网站成功")
                return rs.headers['Set-Cookie']
            else:
                return None

        else:
            return None
    except Exception as e:
        traceback.print_exc()
        return None


def get_cookie():
    for i in range(3):
        cookie = auto_login()
        if cookie:
            return cookie
        time.sleep(3)
    return None




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


# if __name__ == "__main__":
#     login = AutoLogin()
#     login.login()

    # httper = Httper()
    # if not httper.set_cookie(local=True):
    #     if not httper.set_cookie():
    #         httper.set_cookie()
    #
    # post_data = {
    #     "code": "cqssc",
    #     "quantity": 1,
    #     "totalMoney": 2,
    #     "betOrders": [
    #         {
    #             "expect": "20171212100",
    #             "code": "cqssc",
    #             "betCode": "ten_thousand",
    #             "playCode": "one_big_small",
    #             "betNum": "大",
    #             "odd": "1.98",
    #             "betAmount": "1",
    #             "memo": ""
    #         }
    #     ]
    # }
    #
    # rs = httper.post(HttperConstant.BET_URL, data={'betForm': json.dumps(post_data)})
    # print(rs)