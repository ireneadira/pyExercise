# from removebg import RemoveBg
#
# rmbg = RemoveBg('pgQtCdd2K3nFJ9dUZYxLuuvv', 'error.log')
# rmbg.remove_background_from_img_file('C:/Users/Administrator/Desktop/pic/2.jpg')

import requests

"""
短信类,提供功能:发短信
"""
class SMS(object):
    def __init__(self, account, password):
        self.url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"  # 接口地址
        self.account = account  # APIID
        self.password = password  # APIkey

    def send_sms(self, mobiles, content):
        """
        发短信
        :param mobiles: 手机号列表
        :param content: 短信内容
        :return:None
        """
        for mobile in mobiles:
            # 定义请求的头部
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"

            }
            # 定义请求的数据
            data = {
                "account": self.account,
                "password": self.password,
                "mobile": mobile,
                "content": content,
            }
            # 发起数据
            response = requests.post(self.url, headers=headers, data=data)
            print(response.content.decode())


if __name__ == '__main__':
    sms = SMS('C11201818', '8eba2a5f14d14abc7fa683a700bf3b42')
    sms.send_sms(['13883322027'], '您的验证码是：888888。请不要把验证码泄露给其他人。')