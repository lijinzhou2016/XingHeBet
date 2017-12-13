import traceback
import json
import os, sys
import codecs
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
util_dir = os.path.join(base_dir, 'util')
sys.path.append(util_dir)

from bet.httper import Httper
from bet.settings import ReceiveNumberConstant
from util.periods import Periods
from util.common import get_time


class Receive(object):
    def __init__(self, url=ReceiveNumberConstant.RECEIVE_NUMBER_URL,
                 save_number=ReceiveNumberConstant.SAVE_NUMBERS_LOG_FLAG,
                 save_number_file_name = ReceiveNumberConstant.SAVE_NUMBERS_FILE_NAME):
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
        with open(path, 'w') as f:
            f.write(data)

    def __save_number(self, numbers, periods):
        self.__write(self.__save_numbers_file_name, numbers)

        if self.__save_numbers_log_flag:
            file_path = os.path.join(self.__get_save_path(), periods+'.json')
            self.__write(file_path, numbers)

    def __receive_number(self, periods):
        rs = self.__httper.get(self.__url.format(periods))
        if rs is None:
            return None
        else:
            return rs

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
        numbers = self.__receive_number(periods)

        if numbers is None:  # 获取号码失败
            numbers = json.dumps({'isbet':False})
            self.__save_number(numbers, periods)
            return (False, 'Code Server No Response')
        if not numbers['isbet']:  # 此号不买
            self.__save_number(numbers, periods)
            return (False, "Not buy")
        else:   # 正常获取
            self.__save_number(numbers, periods)
            return (True, "Get bet Code Success")


if __name__ == "__main__":
    receive = Receive()
    print(receive.get_numbers())



