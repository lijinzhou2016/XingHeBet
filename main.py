import os
import sys
import time
import json
import traceback

base_dir = os.path.dirname(os.path.abspath(__file__))
bet_dir = os.path.join(base_dir, 'bet')
util_dir = os.path.join(base_dir, 'util')

sys.path.append(base_dir)
sys.path.append(bet_dir)
sys.path.append(util_dir)
from bet.bets import Bets
from util.periods import Periods
from util.common import Delay
from bet.receivenumber import Receive
from util.mylogger import log
from bet.settings import BetsConstant


if __name__ == "__main__":
    bets = Bets()
    periods = Periods()
    delay = Delay()
    receive = Receive()

    bets.init_cookie()
    gid = periods.get_periods()
    before_gid = 0
    while True:
        while periods.is_sleep_time():
            delay.display_time()
        else:
            print()

        # 等待进入新的一期购买时间
        while int(gid) == int(before_gid):
            delay.display_time("  wait " + str(int(gid) + 1))
            gid = periods.get_periods()  # 获取当前期数
        else:
            print()
            if int(before_gid) == 0:
                before_gid = gid
            else:
                before_gid = gid
                if periods.is_interval_10_minute():  # 若10分钟一期，延时2-3分钟购买
                    delay.random_delay(100, 150)
                else:  # 若5分钟一期，延时1-2分钟购买
                    delay.random_delay(50, 100)

        # status, note = receive.receive_and_save()
        # if not status:
        #     log.error(note)
        #     continue

        for loop in range(4):
            try:
                rs = bets.buy_numbers()

                if rs is None:
                    log.error('Bet Server No Response')
                    delay.random_delay(5, 10)
                    continue
                if BetsConstant.BET_SUCCESS_STATUS in rs:
                    log.info(BetsConstant.BET_SUCCESS_STATUS)
                    break
                if BetsConstant.BET_ODD_UPDATE_STATUS in rs:
                    log.error('赔率发生变化')
                    delay.random_delay(5, 10)
                if BetsConstant.BET_COOKIE_OVER_TIME_STATUS in rs:
                    log.error('cookie 失效')
                    bets.reset_cookie()
                    continue
                if BetsConstant.BET_PERIODS_OVER_TIME_STATUS in rs:
                    log.error('该期停止投注')
                    break
            except Exception as e:
                log.error(str(traceback.print_exc()))
                continue
