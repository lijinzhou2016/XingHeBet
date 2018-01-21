import codecs
import json
import os
import sys
import traceback
import requests

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
util_dir = os.path.join(base_dir, 'util')
sys.path.append(util_dir)

from bet.httper import Httper
from settings import ReceiveNumberConstant
from util.periods import Periods
from util.common import get_time
from settings import conf
from common import Delay


class Receive(object):
    def __init__(self, url=conf.get("server_url") + ReceiveNumberConstant.RECEIVE_NUMBER_API,
                 save_number=ReceiveNumberConstant.SAVE_NUMBERS_LOG_FLAG,
                 save_number_file_name=ReceiveNumberConstant.SAVE_NUMBERS_FILE_NAME):
        self.__url = url
        self.__save_numbers_log_flag = save_number
        self.__save_numbers_file_name = save_number_file_name
        self.__periods = Periods()
        self.__httper = Httper()
        self.__save_path = get_time('%Y%m%d')

    def get_periods(self):
        return self.__periods.get_periods()

    def __get_save_path(self):
        path = get_time('%Y%m%d')
        if not os.path.exists(path):
            os.mkdir(path)
            self.__save_path = path
        return self.__save_path

    def __write(self, path, data):
        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(data)

    def __save_number(self, numbers, periods):
        self.__write(self.__save_numbers_file_name, numbers)

        if self.__save_numbers_log_flag:
            file_path = os.path.join(self.__get_save_path(), periods+'.json')
            self.__write(file_path, numbers)

    def __receive_number(self, periods):
        try:
            url = self.__url.format(conf['account'], periods)
            print(url)
            rs = requests.get(url, timeout=10)
            if rs.status_code == 200:
                return rs.text
            else:
                return None
        except Exception as e:
            print(u"请求发号器异常")
            traceback.print_exc()
            return None

    def get_numbers(self):
        try:
            with codecs.open(self.__save_numbers_file_name, 'r', 'utf-8') as f:
                return f.read()
        except Exception as e:
            traceback.print_exc()
            return None

    def receive_and_save(self):
        '''

        :param property:
        :return:  False: 不投注
        '''
        periods = self.get_periods()
        print(periods)
        data = self.__receive_number(periods)

        if data is None:
            return None
        else:
            self.__save_number(data, periods)
            return json.loads(data)

def get_bet_code():
    loop_times = 24
    delay = Delay()
    receive = Receive()
    for loop in range(loop_times):
        data = receive.receive_and_save()
        if not data:
            delay.delay(10)
            continue

        if data['hasDate']:
            if not data['isbet']:
                print("此期不买")
                return None
            else:
                return data

        if (data['isbet']) and (not data["hasDate"]):
            print("没有投注数据")
            return None
        delay.delay(10)
    print("依然没有没有投注数据")
    return None



if __name__ == "__main__":
    print(get_bet_code())



