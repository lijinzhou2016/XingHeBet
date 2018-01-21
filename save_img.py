import requests
import wget

url = 'https://vs5566.net/pcenter/captcha/loginTop.html?t=jcoin3wo'

rs = requests.get(url)
if rs.status_code == 200:
    with open("loginTop.jpeg", 'wb') as f:
        f.write(rs.content)