import json
import time

from bet.httper import Httper
from bet.receivenumber import Receive
from settings import BetsConstant
from util.periods import Periods
import requests
from httper import get_cookie
import traceback
import re


class Bets(object):
    def __init__(self, cookie=""):
        self.__httper = Httper()
        self.__receive = Receive()
        self.__url = ''
        self.__periods = Periods()
        self.__cookie = cookie
        self.__headers = {"cookies": self.__cookie}
        self.__first_token_url = "https://vs5566.net/lottery/ssc/cqssc/index.html"
        self.token = ""

    def set_first_token(self):
        try:
            rs = requests.get(self.__first_token_url, headers=self.get_headers(), timeout=10)
            if rs.status_code == 200:
                html = rs.text
                with open("index.html", 'w') as f:
                    f.write(html)
                lines = html.split("\n")
                for line in lines:
                    rs = re.match('.*<input type="hidden" name="gb.token" value="(.*)"></div>.*', line)
                    if rs:
                        self.token = rs.group(1)
                        break

        except Exception as e:
            print("获取token失败")
            traceback.print_exc()
            time.sleep(3)
            exit(-1)
        pass

    def set_cookie(self, cookie=""):
        if not cookie:
            cookie = get_cookie()
        self.__cookie = cookie
        self.__headers = {"cookies": self.__cookie}


    def get_headers(self):
        return self.__headers

    def post(self, url, data=None, headers=None, timeout=10):
        try:
            rs = requests.post(url, data=data, headers=headers, timeout=timeout)
            if rs.status_code == 200:
                return rs.text
            else:
                return None
        except:
            traceback.print_exc()
            return None

    def __get_numbers(self):
        return json.loads(self.__receive.get_numbers())

    def __format_numbers(self, gid, data):
        gid = str(gid)
        data =data




    def __format_url(self):
        url = BetsConstant.BUY_NUMBERS_URL.format(str(round(time.time(), 3)).replace(".", ""))
        print(url)
        return url

    def buy_numbers(self, gid, data):
        return self.post(self.__format_url(), data=self.__format_numbers(gid, data), headers=self.get_headers())

    def display_numbers(self, data):
        data = data['betOrders']
        for index in range(len(data)):
            del data[index]['expect']
            del data[index]['playCode']
            del data[index]['odd']
            del data[index]['memo']
            del data[index]['code']

        return data



