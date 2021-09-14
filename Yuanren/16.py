# -*- coding: UTF-8 -*-
# @author: zhulw
# @file: 16
# @time: 2020-11-24
# @desc:


import requests
import re
import execjs

session = requests.session()
headers = {
    'Host': 'match.yuanrenxue.com',
    'Pragma': 'no-cache',
    'Referer': 'http://match.yuanrenxue.com/match/16',
    'User-Agent': 'yuanrenxue.project',
    'X-Requested-With': 'XMLHttpRequest'
}
session.headers = headers
sum_ = 0
with open("js/16.js", "r") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

for i in range(1, 6):
    api_url = "http://match.yuanrenxue.com/api/match/16"
    result = ctx.call("get_m")
    print(result)
    params = {
        "page": i,
        "t": result[0],
        "m": result[1]
    }
    r = session.get(api_url, headers=headers, params=params)
    print(r.json())
    data = r.json()["data"]
    for d in data:
        sum_ += d["value"]
print(sum_)
# 213133
