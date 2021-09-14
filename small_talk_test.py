import requests
import time

url_base = "https://www.ddxstxt8.com/3_3255/"
url_page = "427725609.html"


headers = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cookie': 'Hm_lvt_40639e2e855ad00c65304ee021f07859=1615600065,1615788030,1616048835,1617094864; Hm_lpvt_40639e2e855ad00c65304ee021f07859={}'.format(int(time.time()))
}

url = url_base + url_page
response = requests.request("GET", url, headers=headers)
response.encoding = 'gb18030'

print(response.text.replace('&nbsp;', ' ').replace('<br /><br />', '\n'))
