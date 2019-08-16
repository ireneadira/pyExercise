# -*- encoding:utf-8 -*-
import requests
from lxml import etree
import random
import chardet
import time


for page in range(250,280,1):
    url = f'https://yande.re/post?page={page}&tags=wallpaper'
    html = requests.get(url)
    imgs = etree.HTML(html.text)
    imgpath = imgs.xpath("//li/a[@class='directlink largeimg']/@href")
    for i in imgpath:
        with open('picpath.txt','a') as f:
            f.write(i + '\n')
    print(f'NO.{page} completed XD')

#        res = requests.get(i)
#        with open(i.split('/')[-1].replace('%20','_'),'wb') as f:
#            f.write(res.content)

#link = 'https://files.yande.re/image/2723b67bc7bc1464001b2b0810108fb2/yande.re%20560210%20bikini%20calendar%20dress%20see_through%20swimsuits%20wallpaper%20wet_clothes%20yuuki_hagure.jpg'
#                                                                       yande.re 560210 bikini calendar dress see_through swimsuits wallpaper wet_clothes yuuki_hagure.jpg
#                                                                       yande.re_560210_bikini_calendar_dress_see_through_swimsuits_wallpaper_wet_clothes_yuuki_hagure.jpg

with open ('picpath.txt','r') as f:
    for i in f.readlines():
        print(i.split('/')[-1].replace('%20','_'))
