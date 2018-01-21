import re


with open("index.html", 'r') as f:
    html = f.readlines()
    for line in html:
        rs = re.match('.*<input type="hidden" name="gb.token" value="(.*)"></div>.*', line)
        if rs:
            print(rs.group(1))
