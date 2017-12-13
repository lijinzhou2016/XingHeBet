import time
import random

def get_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(time.time()))


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
