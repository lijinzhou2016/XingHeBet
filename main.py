import os
import sys
import traceback
import codecs
import time

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
from settings import BetsConstant
from httper import get_cookie
from settings import conf
from util.sendermsg import Phone, Sender
from users import Users
from bet.receivenumber import get_bet_code


# https://www.vs5566.net/
# bigman971225
# chen971225


ph_list = conf['phone']
ph_obj = Phone()

def send_msg(msg):
    for ph in ph_list:
        sender = Sender(ph)
        sender.send(msg)
        time.sleep(3)

if __name__ == "__main__":

    cookie = get_cookie()
    if not cookie:
        print(u"自动登录失败，请稍后再试")
        time.sleep(3)
        exit(-1)
    bets = Bets(cookie)     # 设置cookies
    bets.set_first_token()  # 下注字token字段

    user = Users()
    if not user.check_user():
        print(u"账号："+conf['account'] + u" 不存在")
        time.sleep(3)
        exit(-1)
    else:
        print(u"=== 自动下注工具账号验证成功")



    periods = Periods()
    delay = Delay()
    receive = Receive()

    gid = periods.get_periods()
    before_gid = 0
    while True:
        while periods.is_sleep_time():  #
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
                    delay.random_delay(120, 180)
                else:  # 若5分钟一期，延时1分钟购买
                    delay.delay(60)

        post_data = get_bet_code()
        if not post_data:
            continue

        log.info(gid)

        for loop in range(4):
            try:
                rs = bets.buy_numbers(gid, post_data)
                # print(rs)

                if rs is None:
                    log.error('Bet Server No Response')
                    delay.random_delay(5, 10)
                    continue
                if BetsConstant.BET_SUCCESS_STATUS in rs:
                    log.info(BetsConstant.BET_SUCCESS_STATUS)
                    break
                if BetsConstant.BET_PARMS_ERROR_STATUS in rs:
                    log.error(BetsConstant.BET_PARMS_ERROR_STATUS)
                    break
                if BetsConstant.BET_COOKIE_OVER_TIME_STATUS in rs:
                    log.error('cookie 失效')
                    bets.set_cookie()
                    continue
            except Exception as e:
                log.error(str(traceback.print_exc()))
                continue
