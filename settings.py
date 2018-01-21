import time
import codecs
import os
import time

class HttperConstant(object):
    COOKIES_FILE_NAME = '.cookies'

    INPUT_COOKIES_NOTE = 'Please Input Cookies:'
    BET_URL = 'https://vs5566.net/lottery/ssc/cqssc/saveBetOrder.html?t={0}'
    COOKIES_KEY = 'SID'
    TEST_COOKIES_DATA = {
        "code": "cqssc",
        "quantity": 1,
        "totalMoney": 1,
        "betOrders": [
            {
                "expect": "20171212090",
                "code": "cqssc",
                "betCode": "ten_thousand",
                "playCode": "one_big_small",
                "betNum": "大",
                "odd": "1.98",
                "betAmount": "1",
                "memo": ""
            }
        ]
    }


class ReceiveNumberConstant(object):
    RECEIVE_NUMBER_API = '/project/PredictionResultServlet?phone={0}&period={1}'
    SAVE_NUMBERS_LOG_FLAG = True
    SAVE_NUMBERS_FILE_NAME = '.numbers.json'


class BetsConstant(object):
    BUY_NUMBERS_URL = 'https://vs5566.net/lottery/ssc/cqssc/saveBetOrder.html?t={0}'
    BET_SUCCESS_STATUS = '下注成功'
    BET_PARMS_ERROR_STATUS = '下注期数已过期'
    BET_ODD_UPDATE_STATUS = '参数有误'
    BET_COOKIE_OVER_TIME_STATUS = 'login.html'
    BET_LOGIN_URL = 'https://vs5566.net/passport/login.html?t={0}'

xinghe_user = ""
xinghe_pwd = ""
yundama_user = ""
yundama_pwd = ""
account = ""
server_url="http://47.104.31.179"
phone = []


def load_config_file():
    global xinghe_pwd, xinghe_user, yundama_pwd, yundama_user, account, phone, server_url

    if os.path.exists("config.txt"):
        with codecs.open("config.txt", 'r', "utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if (not line) or (line.startswith("#")):
                    continue
                if "xinghe_user" in line:
                    xinghe_user = line.split("=")[1].replace("\n","").strip()
                if "xinghe_pwd" in line:
                    xinghe_pwd = line.split("=")[1].replace("\n","").strip()
                if "yundama_user" in line:
                    yundama_user = line.split("=")[1].replace("\n","").strip()
                if "xinghe_user" in line:
                    yundama_pwd = line.split("=")[1].replace("\n","").strip()
                if "account" in line:
                    account = line.split("=")[1].replace("\n","").strip()
                if "phone" in line:
                    phone = line.split("=")[1].replace("\n","").strip().split(",")
                if "server_url" in line:
                    server_url = line.split("=")[1].replace("\n","").strip()

        if not xinghe_user or not xinghe_pwd:
            print("请检查config.txt, xinghe_user 或者 xinghe_pwd没有配置")
            time.sleep(5)
            exit(-1)
        if not yundama_user or not yundama_pwd:
            print("请检查config.txt, yundama_user 或者 yundama_pwd没有配置")
            time.sleep(5)
            exit(-1)
        if not account:
            print("请检查config.txt, account 没有配置")
            time.sleep(5)
            exit(-1)

        return {
            "xinghe_user": xinghe_user,
            "xinghe_pwd": xinghe_pwd,
            "yundama_user": yundama_user,
            "yundama_pwd": yundama_pwd,
            "account": account,
            "phone": phone,
            "server_url": server_url
        }
    else:
        print(u"没有找到config.txt配置")
        time.sleep(5)
        exit(-1)


conf = load_config_file()

