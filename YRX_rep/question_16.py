# -*- encoding:utf-8 -*-
import requests
import execjs
import time


headers = {
  'authority': 'match.yuanrenxue.com',
  'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'x-requested-with': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'yuanrenxue.project',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://match.yuanrenxue.com/match/16',
  'accept-language': 'zh-CN,zh;q=0.9',
}

with open('js_file/16.js', mode='r', encoding='utf-8') as f:
    jsEx = f.read()

p_s = str(int(time.time())) + '000'
m_value = execjs.compile(jsEx).call('get_m', p_s)

url = "https://match.yuanrenxue.com/api/match/16?page=4&m={}&t={}".format(m_value, p_s)
response = requests.request("GET", url, headers=headers)
print(response.text)

