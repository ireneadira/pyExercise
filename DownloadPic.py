# encoding:utf-8
import os
import time
import redis
import random
import requests
from selenium import webdriver

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
pic_path = 'E:/ReptileData/8.14/PicDL/'
if not os.path.exists(pic_path):
    os.mkdir(pic_path)


def get_pic_first_step():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {
        'profile.default_content_setting_values': {
            # 'javascript': 2,
            'images': 2
        }
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
        """})
    driver.set_page_load_timeout(77)
    while r.llen('pic_url_1'):
        get_pic_url = r.lpop('pic_url_1')
        driver.get(get_pic_url)
        time.sleep(random.uniform(0.3, 1.1))
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(random.uniform(0.3, 0.7))
        all_pic_url = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/div[1]/main/project-assets/div/div[1]/div[1]/picture/img')
        for url_2 in all_pic_url:
            pic_url = url_2.get_attribute('src')
            r.rpush('pic_url_2', pic_url)
            print('PUSH : ' + pic_url)

def get_pic_second_step():
    while r.llen('pic_url_2'):
        try:
            head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                    'Connection': 'close'}
            pic_url = r.lpop('pic_url_2') # http://pfs.pinduoduo.com/ottawa-api/medicine/order/07D8DC9FB05D48D09B4372AAC77D8F85_ext.jpg?sign=q-sign-algorithm%3Dsha1%26q-ak%3DSeuLoyNJ2o4fTOsDj8jhNEuCUUSHr76z%26q-sign-time%3D1628816832%3B1628831232%26q-key-time%3D1628816832%3B1628831232%26q-header-list%3D%26q-url-param-list%3D%26q-signature%3D710ed593ba621c37cd6d8e69e885c818a1f16db3
            pic_url_list = pic_url.split('/')
            html = requests.get(pic_url, headers=head, timeout=5)
            pic_name = pic_url_list[-1][:32] + '.jpg'
            pic_path_tmp = pic_path
            if not os.path.exists(pic_path_tmp):
                os.mkdir(pic_path_tmp)
            if html.status_code == 200:
                with open(pic_path_tmp + pic_name, "wb") as f:
                    f.write(html.content)
            print('get a pic : ' + pic_name)
        except Exception as err:
            print(err)
            continue


if __name__ == '__main__':
    get_pic_second_step()


