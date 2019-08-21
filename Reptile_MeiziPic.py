# -*- coding: utf-8 -*-
import threading
import requests
import time
import os
from lxml import etree
from time import sleep
from queue import Queue
from threading import Thread


# 传入数据: url:网址 rootpath:图片页所在标题作为本地存储根目录
class reptileMeizi():
    def __init__(self):
        self.picQueue = Queue()
        for i in range(5521,1,-1):
            url = f'https://www.meizitu.com/a/{i}.html'
            self.picQueue.put(url)
            print('put completed XD')

    # 开启程序 调用下方函数
    def startMain(self, threadName):
        try:
            Url = self.picQueue.get()
            print(f"Thread {threadName} get a picLink : {Url}")
            rootPath, picList = self.getPicpath(Url)
            if len(picList) > 0:
                self.saveToLocal(rootPath, picList)
        except Exception as err:
            print(err)

    # 从url中获取所有图片链接
    def getPicpath(self, Url):
        html = requests.get(Url)
        html.encoding = 'gb18030'
        if html.status_code == 200:
            xml_path = etree.HTML(html.text)
            picList = xml_path.xpath("//div[@id='picture']/p/img/@src")
            Rootpath = xml_path.xpath("//h2/a")
            rootPath = Rootpath[0].text
            print('Title(Folder) is : ' + str(rootPath))
            print('get picture List success XD')
            return rootPath,picList

    # 接收图片链接 存本地
    def saveToLocal(self, rootPath, picList):
        saveToPath = 'MeiZiPic/' + rootPath + '/'
        if not os.path.exists(saveToPath):
            os.makedirs(saveToPath)
        for picLink in picList:
            picName = picLink.split('/')[-1]
            print(f'get {picLink}')
            html = requests.get(picLink)
            if html.status_code == 200:
                with open(saveToPath + picName,"wb") as f:
                    f.write(html.content)
            else:
                print('pic Link Error X(')
                break

    # 多线程模块
    def startThread(self):
        while True:
            threadList = []
            for threadName in range(5):
                thread = Thread(target=self.startMain ,args=(threadName,))
                threadList.append(thread)
                thread.start()
            for wait in threadList:
                wait.join()

if __name__ == '__main__':
    # tempLate = 'https://www.meizitu.com/a/5521.html' # first Page
    reptile = reptileMeizi()
    reptile.startThread()
