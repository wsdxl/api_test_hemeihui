"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/24 17:04
E-mail  : 506615839@qq.com
file:   test_dongtaijubao.py
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
from common.hande_db import HandDB

data_path = os.path.join(DataDir, 'shaibaoquan.xlsx')


@ddt
class TestDongTaiJuBao(unittest.TestCase):
    excel = ReadExcel(data_path, 'dongtaijubao')
    datas = excel.read_excel()
    http = HanderRequest()
    db = HandDB()

    @classmethod
    def setUpClass(cls):
        my_login = Login()
        sid, chainRole = my_login.login()
        setattr(TestData, 'sid', sid)

    def setUp(self):
        sql = 'select id from fybanks_hfjyuan.dynamic_info where id not in (select dynamic_comment_id from fybanks_hfjyuan.dynamic_report where type=1) and status=3 and state=1 order by id desc'
        id = self.db.get_one(sql)[0]
        setattr(TestData, 'id', str(id))
        sql1 = 'select id from fybanks_hfjyuan.dynamic_comment where id not in (select dynamic_comment_id from fybanks_hfjyuan.dynamic_report where type=2) and state=1 order by id desc'
        pid = self.db.get_one(sql1)[0]
        setattr(TestData, 'pid', str(pid))

    @data(*datas)
    def test_dongtaijubao(self, case):
        # 获取url地址
        case['url'] = replace_data(case['url'])
        url = conf.get('hfjyuan', 'url') + case['url']
        method = case['method']
        case['data'] = replace_data(case['data'])
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
            if case['interface'] =='动态举报' and res['msg']=='success':
                sql=replace_data(case['check_sql'])
                report_type=self.db.get_one(sql)[0]
                self.assertEqual(data['reportType'],report_type)
            if case['interface'] =='评论举报' and res['msg']=='success':
                sql1=replace_data(case['check_sql'])
                report_type1=self.db.get_one(sql1)[0]
                self.assertEqual(data['reportType'],report_type1)
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

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
