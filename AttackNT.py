# -*- coding: utf-8 -*-
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.set_page_load_timeout(3)

try:
    driver.get('https://item.jd.com/100009085723.html')
    print('finish load ....')
except Exception:
    driver.execute_script('window.stop()')
    print(driver.find_element_by_xpath('//*[@id="pingou"]/div/div/div[1]/div[2]/span/span[2]').text)
    print(driver.title)
finally:
    driver.quit()

