"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/25 17:39
E-mail  : 506615839@qq.com
file:   test_dongtaibianji.py
============================
"""
import os
import unittest
from library.ddt import ddt,data
from common.contans import DataDir
from common.read_excel import ReadExcel
from common.login import Login
from common.hander_data import TestData,replace_data
from common.read_conf import conf
from common.hander_request import HanderRequest
from common.my_logger import my_logger
from common.hande_db import HandDB

data_path=os.path.join(DataDir,'shaibaoquan.xlsx')
@ddt
class TestDongTaiBiaoJi(unittest.TestCase):
    excel=ReadExcel(data_path,'dongtaibianji')
    datas=excel.read_excel()
    http=HanderRequest()
    db=HandDB()

    @classmethod
    def setUpClass(cls):
        my_login = Login()
        sid, chainRole = my_login.login()
        setattr(TestData, 'sid', sid)

    def setUp(self):
        sql='select id from fybanks_hfjyuan.dynamic_info order by id desc'
        id=self.db.get_one(sql)[0]
        setattr(TestData,'id',str(id))

    @data(*datas)
    def test_dongtaibianji(self,case):
        # 准备用例数据
        case['url'] = replace_data(case['url'])
        url = conf.get('hfjyuan', 'url') + case['url']

        method = case['method']
        case['data']=replace_data(case['data'])
        data = eval(case['data'])
        expected = eval(case['expected'])
        headers = eval(case['headers'])
        row = case['case_id'] + 1
        # 发送请求
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
            my_logger.info('用例-->{}:执行已通过'.format(case['title']))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

