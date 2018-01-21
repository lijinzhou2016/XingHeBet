import requests
import time
import json


betorders = [
    {
        "expect": "20171212066",
        "code": "cqssc",
        "betCode": "ten_thousand",
        "playCode": "one_big_small",
        "betNum": "大",
        "odd": "1.98",
        "betAmount": "2",
        "memo": ""
    },
    {
        "expect": "20171212066",
        "code": "cqssc",
        "betCode": "hundred",
        "playCode": "one_single_double",
        "betNum": "单",
        "odd": "1.98",
        "betAmount": "3",
        "memo": ""
    }
]
post_data = {
    "code": "cqssc",
    "quantity": 1,
    "totalMoney": 2,
    "betOrders": [
        {
            "expect": "20180121092",
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
post_headers ={
    'Cookie':'UM_distinctid=160b06072cf2f2-00f1098e3443e5-16386656-13c680-160b06072d0349; isAutoPay=true; BALANCE_HIDE=false; REFRESH_BALANCE_TIME=0; CNZZDATA1264553986=759449776-1514783287-%7C1516538240; SID=ym9VAhibBCCYOWFR0X7sK3tMx0pP8gUT6vthX49g+oA52arlOw3aZLsOAwWP4Hd8lUlk8khoiAzYSYgYs/JOcA==; route=804e8ed353920e1bb6689a6b84113903',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

}

post_url = 'https://vs5566.net/lottery/ssc/cqssc/saveBetOrder.html?t={0}'.format(str(round(time.time(), 3)).replace(".",""))
# print(post_data)
print(post_url)
#
rs = requests.post(post_url, headers=post_headers, data={"gb.token":"a4dd09fb-940d-48db-b196-0f37c2c38638",'betForm': json.dumps(post_data)})
print(rs.text)
# if 'login.html' in rs.text:
#     print("hhhhh")

# post_type_url = 'https://vs5566.net/lottery/commonLottery/getRecent5Records.html?t={0}'.format(str(round(time.time(), 3)).replace(".",""))
# post_type_data = {'code': 'cqssc'}

# rs = requests.post(post_type_url, data=post_type_data)
# print(rs.text)