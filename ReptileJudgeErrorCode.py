import requests
import re

def get_codetype(title_code):
    judge_err = re.compile("([\u4E00-\u9FA5]|[\u0030-\u0039]|[\u0041-\u005a]|[\u0061-\u007a])",re.S) 
    ju_list = judge_err.findall(title_code)
    title_len = len(title_code)
    ju_len = len(ju_list)
    if title_len - int(title_len/5) <= ju_len or title_len == 0:
        return True
    else:
        return False

def replit_title(id_num, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
    codetype = ['utf-8','gb2312']
    try:
        req = requests.get(url, headers=headers, stream=True, timeout=7)
    except:
        # self.updatebase(id_num,'errX(')
        print('访问出错')
        return 0
    # 判断长度是否为下载链接
    try:
        ju_len = req.headers['Content-Length']
        ju_len = int(ju_len)
        print('may download %d' % ju_len)
    except:
        try:
            ju_len = len(req.text)
            print('may url %d' % ju_len)
        except:
            # self.updatebase(id_num,'errX(')
            print('未知错误')
            return 0
    if ju_len < 999999:
        # 获取字符类型
        try:
            ju_code = False
            for ctype in codetype:
                req.encoding = ctype
                title = re.findall('<title>(.*?)</title>',req.text)[0][:255].replace('&nbsp;','')
                ju_code = get_codetype(title)
                if ju_code == True:
                    break
            if ju_code:
                # self.updatebase(id_num,title)
                print('有标题 : ' + title)
            else:
                print('是乱码 : ' + title)
        except:
            # self.updatebase(id_num,0)
            print('正则没匹配到标题')
    else:
        # self.updatebase(id_num,1)
        print('下载链接')



if __name__ == '__main__':
    url = 'm.rar8.net/Soft/91888.html'
    link = 'http://' + url
    replit_title(0, link)
