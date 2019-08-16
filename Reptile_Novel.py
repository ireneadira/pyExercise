# -*- encoding:utf-8 -*-
import requests
from lxml import etree
import random
import chardet
import time
 
if __name__=='__main__':
    url = 'http://nuansy.cn/zetianji/293.html'
    while True:
        link = url[:16]
        #通过get方式打开页面
        response = requests.get(url)
        #获取页面内容
        html = response.content
        #判断页面使用的字符集
        charset = chardet.detect(html)
        #print(charset)
        response.encoding='utf-8'

        filter_x = etree.HTML(response.text)
        xs_content = filter_x.xpath("//div[@class='content']//p")
        next_page = filter_x.xpath("//div[@class='row-fluid bottomlink hidden-phone']/div/a[last()]/@href")
        if 'javas' in next_page[0]:
            print('commmmmmmmmm ............................')
            break
        for i in xs_content:
            if i.text == None:
                continue
            with open ('zetianji.txt', 'a+' ,encoding='utf-8') as f:
                f.write(i.text + '\n')
        url = link + next_page[0]
        time.sleep(1)
        print(url)
    

# //div[@class='bottomlink visible-phone text-center']/a[last()]/@href  #下一章按钮
    
    #打印输出
    # print(str(html,'utf-8'))