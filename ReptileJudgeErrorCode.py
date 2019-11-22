import requests
import re

# 判断是否含有乱码 乱码超过20% 则判定该title是乱码 返回False
def get_codetype(title_code):
    judge_err = re.compile("([\u4E00-\u9FA5]|[\u0020-\u007E]|[\u3008-\u3011]|\u00A0)",re.S)
    ju_list = judge_err.findall(title_code)
    title_len = len(title_code)
    ju_len = len(ju_list)
    if title_len - int(title_len/5) <= ju_len or title_len == 0:
        return True
    else:
        return False

# 访问网页正则匹配标题
def replit_title(id_num, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
    codetype = ['utf-8','gb18030'] # 如果觉得18030太长则用 gb2312
    try:
        req = requests.get(url, headers=headers, stream=True, timeout=7)
    except:
        print('Access Error')
        return 0
    # 判断长度是否为下载链接
    try:
        ju_len = req.headers['Content-Length']
        ju_len = int(ju_len)
        print('may download link len : %d' % ju_len)
    except:
        try:
            ju_len = len(req.text)
            print('normal link len : %d' % ju_len)
        except:
            print('Unknow Error')
            return 0
    if ju_len < 999999:
        try:
            ju_code = False
            for ctype in codetype:
                req.encoding = ctype
                title = re.findall('<title>(.*?)</title>',req.text)[0][:255].replace('&nbsp;','')
                ju_code = get_codetype(title)
                if ju_code == True:
                    break
            if ju_code:
                print('Title : ' + title)
            else:
                print('Have Error Code : ' + title)
        except:
            print('No search Title')
    else:
        print('Download Link')

if __name__ == '__main__':
    url = 'm.rar8.net/Soft/91888.html'
    test_url = 'http://' + url
    replit_title(0, test_url)
