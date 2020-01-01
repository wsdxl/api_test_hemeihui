"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/23 17:05
E-mail  : 506615839@qq.com
file:   test_sousuoshangpin.py
============================
"""
import unittest
import os
from common.read_excel import ReadExcel
from common.contans import DataDir
from library.ddt import ddt, data
from common.hander_data import TestData, replace_data
from common.read_conf import conf
from common.hander_request import HanderRequest
from common.my_logger import my_logger
from common.login import Login

data_path = os.path.join(DataDir, 'shaibaoquan.xlsx')

@ddt
class TestSouSuoShangPin(unittest.TestCase):
    excel = ReadExcel(data_path, 'sousuoshangpin')
    datas = excel.read_excel()
    http = HanderRequest()

    @classmethod
    def setUpClass(cls):
        my_login = Login()
        sid, chainRole = my_login.login()
        setattr(TestData, 'sid', sid)

    @data(*datas)
    def test_sousuoshangpin(self, case):
        # 获取url地址
        url=conf.get('hfjyuan', 'url') + replace_data(case['url'])
        method = case['method']
        data = eval(case['data'])
        headers = eval(case['headers'])
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.http.send(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 断言
        try:
            self.assertEqual(expected['state'], res['state'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            self.excel.write_excel(row=row, column=11, value='未通过')
            my_logger.info('用例-->{}:执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=row, column=11, value='已通过')
            my_logger.info('用例-->{}:执行未通过'.format(case['title']))
