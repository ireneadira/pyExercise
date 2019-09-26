from selenium import webdriver
import requests
import execjs
import re
import os

# headers_1 未访问前的headers
headers_1 = {
"Referer": "http://www.beian.miit.gov.cn/icp/publish/query/icpMemoInfo_showPage.action",
"Cache-Control": "max-age=0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
"Accept-Encoding": "gzip, deflate",
"Host": "www.beian.miit.gov.cn",
"Connection": "Keep-Alive"
}

# 第二次访问所携带的headers
headers_2 = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
"Accept-Encoding": "gzip, deflate",
"Host": "www.beian.miit.gov.cn",
"Connection": "Keep-Alive",
}

# "Cookie": "__jsluid_h=5204b625eade136c51b0eb3f31f31bc8; __jsl_clearance=1569216821.114|0|pqpny3Pj21I%2BpAf95jogoOQgIw4%3D"

url = 'http://www.beian.miit.gov.cn/icp/publish/query/icpMemoInfo_searchExecute.action'

# 第一次访问  第一次访问后带回来cookie和代渲染js代码
r = requests.get(url, headers=headers_1)
# print(r.text)
print(r.status_code)

# 获取需要的JS代码 清洗 处理 渲染
js_code = re.findall(r'<script>(.*?)</script>', r.text)
js = js_code[0]
js = js.replace('eval(','var gcoo = (')
# 运行编译js代码 生成ctx 上下文对象
ctx = execjs.compile(js)
zzz = ctx.eval('gcoo')
c_start = zzz.find('cookie')
c_end = zzz.find("+';Expires=")
cookie_code = zzz[c_start:c_end]
cookie_js = 'var ' + cookie_code + ';return cookie;'   # 如果调用Chrome来渲染js 则需要return
# cookie_js = 'var ' + cookie_code + ';'
print(cookie_js)

# js_925 = "var cookie='__jsl_clearance=1569317125.289|0|'+(function(){var _1m=[[(-~{}|2)],[2-~(+[])-~(-~[(-~{}<<-~{})])],[-~{}]+[(-~{}|2)],[-~{}]+(-~{}-~{}+[]),[-~!/!/-~[(-~{}<<-~{})]+(-~!/!/+[(+!![[]][(+![][{}])])])/[(-~{}<<-~{})]],(-~{}-~{}+[]),[~~{}],(2-~(-~[(-~{}<<-~{})])+[]+[[]][0]),[-~{}]+[~~{}],[-~{}]+[-~{}],[-~{}]+(2-~(-~[(-~{}<<-~{})])+[]+[[]][0]),[-~{}],(-~((-~{}<<-~{})+(-~{}<<-~{}))+[[]][0]),[(-~!/!/+[-~{}-~{}]>>-~{}-~{})-~-~{}+(-~{}|-~-~{})],[-~{}]+(-~((-~{}<<-~{})+(-~{}<<-~{}))+[[]][0]),[(-~-~{}<<-~[])],[-~{}]+[2-~(+[])-~(-~[(-~{}<<-~{})])],[-~{}]+[(-~-~{}<<-~[])]],_26=Array(_1m.length);for(var _16=0;_16<_1m.length;_16++){_26[_1m[_16]]=['PCDKx','Z%','xp',(-~((-~{}<<-~{})+(-~{}<<-~{}))+[[]][0]),'BX',[(-~!/!/+[-~{}-~{}]>>-~{}-~{})-~-~{}+(-~{}|-~-~{})]+(!/!/+[]).charAt((-~!/!/+[-~{}-~{}]>>-~{}-~{})),({}+[[]][0]).charAt(-~{}),({}+[]+[[]][0]).charAt((-~{}<<-~{})),(-~{}-~{}+[])+({}+[[]][0]).charAt(-~((-~{}<<-~{})+(-~{}<<-~{})))+[!''+[]+[[]][0]][0].charAt((+[]))+[(-~-~{}<<-~[])],'g',[(-~{}|2)],'v','VK',(-~{}-~{}+[]),'%',[(-~{}|2)]+[((-~!/!/+[-~{}-~{}]>>-~{}-~{}))/(+!![[]][1])+[]+[[]][0]][0].charAt((-~{}|2)),'D',[-~!/!/-~[(-~{}<<-~{})]+(-~!/!/+[(+!![[]][(+![][{}])])])/[(-~{}<<-~{})]]+[(-~!/!/+[-~{}-~{}]>>-~{}-~{})-~-~{}+(-~{}|-~-~{})]][_16]};return _26.join('')})();return cookie;"

#调用Chrome来渲染JS
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362')
browser = webdriver.Chrome(options=options)
# browser.get('https://www.baidu.com')
cookie = browser.execute_script(cookie_js)
print(cookie)

# 使用phantomJS无头浏览器渲染JS
# os.environ["EXECJS_RUNTIME"] = "PhantomJS"
# node = execjs.get()
# ctx = node.compile(cookie_js)
# js_encode = 'cookie'
# cookie = ctx.eval(js_encode)
# print(cookie)


cooke_value = r.headers['Set-Cookie'].split(' ')[0] + cookie + ';'
cookie_dict = {"Cookie": cooke_value}
headers_2.update(cookie_dict)

print(headers_2)
r = requests.get(url, headers=headers_2)

print(r.status_code)
