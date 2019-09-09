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
class reptileHpic():
    def __init__(self):
        self.picQueue = Queue()
        self.urlQueue = Queue()
        self.url_host = 'http://www.bs935.com'  # 主机名 拼接获取url和下一页的 link
        self.next_page = 'http://www.bs935.com/html/part/index16_35.html'  # 首个要爬的界面
        print('put this station link completed XD')

    # 开启程序 调用下方函数
    def startMain(self, threadName):
        while True:
            if self.urlQueue.empty():
                break
            Url = self.urlQueue.get()
            print(f"Thread {threadName} get a picLink : {Url}")
            rootPath, picList = self.getPicpath(Url)
            if len(picList):
                self.saveToLocal(rootPath, picList)

    # 从主页爬取页面链接 -> 爬取图片
    def get_pic_page(self, homeUrl):
        html = requests.get(homeUrl)
        html.encoding = 'gb18030'
        x_con = etree.HTML(html.text)
        page_list = x_con.xpath("//ul[@class='textList']/li/a/@href") # 取url
        for i in page_list:
            self.urlQueue.put(self.url_host + i)
        next_page = x_con.xpath("//div[@class='pageList']/a[12]/@href") # 取next
        self.next_page = self.url_host + next_page[0]
        print('NEXT:' + self.next_page)

    # 从url中获取所有图片链接
    def getPicpath(self, Url):
        html = requests.get(Url)
        html.encoding = 'gb18030'
        if html.status_code == 200:
            xml_path = etree.HTML(html.text)
            picList = xml_path.xpath("//img/@src")
            Rootpath = xml_path.xpath("//title")
            rootPath = Rootpath[0].text.replace('_亚洲性图','')
            print('Title(Folder) is : ' + str(rootPath))
            print('get picture List success XD')
            return rootPath,picList

    # 接收图片链接 存本地
    def saveToLocal(self, rootPath, picList):
        saveToPath = 'MeiZiPic/' + rootPath + '/'
        if not os.path.exists(saveToPath):
            os.makedirs(saveToPath)
        for picLink in picList:
            picLink = picLink.strip()
            picName = picLink.split('/')[-1]
            print(f"get {rootPath[:2]}/{picName}")
            try:
                html = requests.get(picLink, timeout=30)
                if html.status_code == 200:
                    with open(saveToPath + picName,"wb") as f:
                        f.write(html.content)
                else:
                    print('pic Link Error X(')
            except Exception as e:
                print('ERROR  -> ' + picLink)
                print(e)     

    # 多线程模块
    def startThread(self):
        while True:
            next_page = self.next_page
            if self.urlQueue.empty():
                self.get_pic_page(self.next_page)
                if self.urlQueue.empty():
                    break
            threadList = []
            for threadName in range(7):
                thread = Thread(target=self.startMain ,args=(threadName,))
                threadList.append(thread)
                thread.start()
            for wait in threadList:
                wait.join()
            if next_page == self.next_page:
                break


if __name__ == '__main__':
    # url_host = 'http://www.bs935.com'
    # url = 'http://www.bs935.com/html/part/index16.html'  # //ul[@class='textList']/li/a/@href   NEXT: /html/part/index16_2.html
    # http://www.bs935.com/html/article/index8048.html
    #                     /html/article/index8048.html

    # reptile = reptileMeizi()
    # reptile.startThread()
    # print('unbeliveable XD')
    reptile = reptileHpic()
    reptile.startThread()
    print('unbeliveable XD')




