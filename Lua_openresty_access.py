import requests,random

# 访问网页正则匹配标题
def replit_test(ip, times):
    headers = {'X-Forwarded-For':ip}
    for i in range(times):
        try:
            req = requests.get(url='http://test.com/test', headers=headers, timeout=7)
            if req.status_code == 200:
                print(req.text + f'times is : {i + 1}')
            else:
                print('Access Reject')
                break
        except:
            print('Access Error')
            return 0
        finally:
            req.close()

def random_access(circle_num):
    circle = 0
    while circle < circle_num:
        rand_num = random.randint(170,177)
        ip_addr = '1.1.1.' + str(rand_num)
        acc_times = random.randint(0,100)
        replit_test(ip_addr, acc_times)
        circle += 1

if __name__ == '__main__':
    circle_num = 7
    random_access(circle_num)