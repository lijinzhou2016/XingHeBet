#!/usr/bin/env python
# coding:utf-8

import time
import os
import sys
import json
import traceback
from jsondata import TIME_PERIODS_JSON
from common import get_time


class Periods(object):
    def __init__(self):
        self.__hour = 0
        self.__min = 0
        self.__periods = ''

    def is_interval_10_minute(self):
        self.__refresh_time()
        if (self.__hour > 9 and self.__hour < 22) or (self.__hour == 9 and self.__min >= 50):
            return True
        else:
            return False

    def is_sleep_time(self):
        self.__refresh_time()
        if (self.__hour > 1 and self.__hour <9) or (self.__hour == 1 and self.__min >= 50) or (self.__hour == 9 and self.__min < 50):
            return True
        else:
            return False

    def __get_today(self):
        return get_time(format="%Y%m%d")

    def __get_time_periods_map(self):
        return TIME_PERIODS_JSON

    def __refresh_time(self):
        t = time.localtime()
        self.__hour = t.tm_hour
        self.__min = t.tm_min

    def get_periods(self):
        self.__refresh_time()

        hour_key = str(self.__hour)
        min_key = str(int(self.__min/5)*5)
        if self.is_interval_10_minute():
            min_key = str(int(self.__min/10)*10)

        periods_map = self.__get_time_periods_map()
        try:
            self.__periods = self.__get_today() + periods_map[hour_key][min_key]
            return self.__periods
        except Exception as e:
            traceback.print_exc()
            print(str(self.__hour) + " " + str(self.__min))
            print(str(hour_key) + " " + str(min_key))
            return ""


if __name__ == "__main__":
    pe = Periods()
    print(pe.get_periods())
