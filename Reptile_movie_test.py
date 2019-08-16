# -*- encoding:utf-8 -*-
import requests
from lxml import etree
import random
import chardet
import time

# https://www.88ys.cc/vod-play-id-58547-src-1-num-1.html 电影地址
import requests
import os
import time
from multiprocessing import Pool

def run(i):
    url = 'https://cdn.mb33.vip/20190822/jLUkKkU5/1200kb/hls/z6hzo849%04d.ts'%i
    print("开始下载："+url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
    r = requests.get(url, headers = headers)
    # print(r.content)
    with open('temp_movie/{}'.format(url[-15:]),'wb') as f:
        f.write(r.content)

def merge(t,cmd):
    time.sleep(t)
    res=os.popen(cmd)
    print(res.read())

if __name__ == '__main__':
    # 创建进程池，执行10个任务
    pool = Pool(10)
    for i in range(8921,8922,1):
        pool.apply_async(run, (i,)) #执行任务
    pool.close()
    pool.join()
    #调用合并
    merge(5,"copy /b temp_movie\\*.ts temp_movie\\new.ts")
    print('ok！处理完成')