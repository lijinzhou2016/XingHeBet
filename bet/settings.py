import time

class HttperConstant(object):
    COOKIES_FILE_NAME = '.cookies'
    INPUT_COOKIES_NOTE = 'Please Input Cookies:'
    BET_URL = 'https://vs5566.net/lottery/ssc/cqssc/saveBetOrder.html?t={0}'
    COOKIES_KEY = 'SID'
    TEST_COOKIES_DATA = {
        "code": "cqssc",
        "quantity": 1,
        "totalMoney": 2,
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
    RECEIVE_NUMBER_URL = ''
    SAVE_NUMBERS_LOG_FLAG = True
    SAVE_NUMBERS_FILE_NAME = '.numbers.json'


class BetsConstant(object):
    BUY_NUMBERS_URL = 'https://vs5566.net/lottery/ssc/cqssc/saveBetOrder.html?t={0}'
    BET_SUCCESS_STATUS = '下注成功'
    BET_PERIODS_OVER_TIME_STATUS = '下注期数已过期'
    BET_ODD_UPDATE_STATUS = '参数有误'
    BET_COOKIE_OVER_TIME_STATUS = 'login.html'

