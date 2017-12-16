import time
import json

from bet.httper import Httper
from bet.receivenumber import Receive
from bet.settings import BetsConstant
from util.periods import Periods


class Bets(object):
    def __init__(self):
        self.__httper = Httper()
        self.__receive = Receive()
        self.__url = ''
        self.__periods = Periods()


    def init_cookie(self):
        if not self.__httper.set_cookie(local=True):
            self.reset_cookie()

    def reset_cookie(self):
        if not self.__httper.set_cookie():
            if not self.__httper.set_cookie():
                exit(-1)

    def __get_numbers(self):
        return json.loads(self.__receive.get_numbers())

    def __format_numbers(self, gid, data):
        data = json.loads(data)
        data['betOrders'][0]["expect"] = str(gid)
        return {'betForm': json.dumps(data)}

    def __format_url(self):
        return BetsConstant.BUY_NUMBERS_URL.format(str(round(time.time(), 3)).replace(".", ""))

    def buy_numbers(self, gid, data):
        return self.__httper.post(self.__format_url(), data=self.__format_numbers(gid, data))

    def display_numbers(self, data):
        data = json.loads(data)['betOrders']
        for index in range(len(data)):
            del data[index]['expect']
            del data[index]['playCode']
            del data[index]['odd']
            del data[index]['memo']
            del data[index]['code']

        return data


