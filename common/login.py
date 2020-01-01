'''
============================
Author  : XiaoLei.Du
Time    : 2019/12/6 10:43
E-mail  : 506615839@qq.com
File    : login_com.py
============================
'''
import os
import requests
import jsonpath
from common.read_conf import conf
from common.hander_request import HanderRequest


class Login:
    login_data = {
        "areacode": conf.get('hfjyuan','areacode'),
        "password": conf.get('hfjyuan','password'),
        "phone": conf.get('hfjyuan','phone')
    }

    def login(self,login_data=login_data):
        base_url = conf.get('hfjyuan', 'url')
        header = eval(conf.get('hfjyuan', 'header'))
        login_url = conf.get('hfjyuan', 'login_url')
        req = HanderRequest()
        url = base_url + login_url

        response = req.send(url=url, method='post', data=login_data, headers=header)
        res = response.json()
        sid = jsonpath.jsonpath(res, '$..sid')[0]
        chainRole = jsonpath.jsonpath(res, '$..chainRole')[0]
        return sid, chainRole


if __name__ == '__main__':
    my_login = Login()
    sid, chainRole = my_login.login()
    print(sid, chainRole)
