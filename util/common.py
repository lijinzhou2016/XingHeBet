import time
import random

def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))

def ten_to_36(n):
    map_ = {
        "0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5",
        "6": "6", "7": "7", "8": "8", "9": "9", "10": "a", "11": "b",
        "12": "c", "13": "d", "14": "e", "15": "f", "16": "g", "17": "h",
        "18": "i", "19": "j", "20": "k", "21": "l", "22": "m", "23": "n",
        "24": "o", "25": "p", "26": "q", "27": "r", "28": "s", "29": "t",
        "30": "u", "31": "v", "32": "w", "33": "x", "34": "y", "35": "z"
    }
    yushu_list = list()
    if int(n) < 36:
        return str(n)

    while int(n) > 36:
        n, yushu = divmod(int(n), 36)
        # print(str(n)+" - "+str(yushu))
        yushu_list.append(str(yushu))

    return map_[str(n)] + "".join([map_[y] for y in yushu_list][::-1])


def get_login_time_stamp():
    t = str(time.time()).replace(".","")[:13]
    # print(t)
    return ten_to_36(t)



class Delay(object):

    def delay(self, t):
        tt = range(t)
        tt = list(tt)
        tt.reverse()
        for tp in tt:
            print("\r" + "Total Delay: " + str(t) + "  " + "Leave: " + str(tp) + "  ", end="")
            time.sleep(1)
        print()

    def random_delay(self, start=1, stop=5):
        t = random.randint(start, stop)
        self.delay(t)

    def display_time(self, note=""):
        t = get_time()
        print('\r' + t + note, end="   ")
        time.sleep(1)


