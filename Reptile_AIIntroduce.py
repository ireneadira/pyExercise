# -*- encoding:utf-8 -*-
import requests
from lxml import etree

url = 'https://www.captainbed.net/2018/11/18/whatisnn/'

while True:
    res = requests.get(url)
    res.encoding='utf-8'
    xetree = etree.HTML(res.text)
    title = xetree.xpath("//h1/a")
    conte = xetree.xpath("//div[@class='entry-content e-content']/p")
    nextp = xetree.xpath("//div[@class='nav-next']/a/@href")
    try:
        print(title[0].text)
    except:
        break

    with open ('AItrach.txt','a',encoding='utf-8') as f:
        f.write(str(title[0].text) + '\n')

    for i in conte:
        if i.text == None:
            with open ('AItrach.txt','a',encoding='utf-8') as f:
                f.write('PIC ->' + '\n')
                continue
        with open ('AItrach.txt','a',encoding='utf-8') as f:
            f.write(str(i.text) + '\n')

    url = nextp[0]
