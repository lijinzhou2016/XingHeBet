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
            "expect": "20171213063",
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
    'Cookie':'SID=C2YoCU9cXQqkO8zuQhU5/ZGOkfvL3Z0On71X/EYfIK9YptwAeQa7LyzTjweDw0D3Op0hwD31s5gdQnDvc9iu+g=='
}

post_url = 'https://vs5566.net/lottery/ssc/cqssc/saveBetOrder.html?t={0}'.format(str(round(time.time(), 3)).replace(".",""))
# print(post_data)
# print(post_url)
#
rs = requests.post(post_url, headers=post_headers, data={'betForm': json.dumps(post_data)})
print(rs.text)
# if 'login.html' in rs.text:
#     print("hhhhh")

# post_type_url = 'https://vs5566.net/lottery/commonLottery/getRecent5Records.html?t={0}'.format(str(round(time.time(), 3)).replace(".",""))
# post_type_data = {'code': 'cqssc'}

# rs = requests.post(post_type_url, data=post_type_data)
# print(rs.text)