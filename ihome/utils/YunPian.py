import requests
import json


class Yunpian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey': self.api_key,
            'text': '【史新天】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code),
            'mobile': mobile
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict
        # print(re_dict)


if __name__ == '__main__':
    yun_pian = Yunpian('9e2ca7e473cfa3cf36a078fed9f8dba7')
    yun_pian.send_sms('201777', '13269463799')
