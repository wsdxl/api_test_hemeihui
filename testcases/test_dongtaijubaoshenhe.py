"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/25 16:00
E-mail  : 506615839@qq.com
file:   test_dongtaijubaoshenhe.py
============================
"""
import os
import unittest
from library.ddt import ddt, data
from common.contans import DataDir
from common.read_excel import ReadExcel
from common.read_conf import conf
from common.hander_data import TestData, replace_data
from common.hander_request import HanderRequest
from common.my_logger import my_logger
from common.hande_db import HandDB

data_path = os.path.join(DataDir, 'shaibaoquan.xlsx')


@ddt
class TestDongTaiJuBaoShenHe(unittest.TestCase):
    excel = ReadExcel(data_path, 'dongtaijubaoshenhe')
    datas = excel.read_excel()
    http = HanderRequest()
    db = HandDB()

    def setUp(self):
        sql = 'select id,dynamic_comment_id from fybanks_hfjyuan.dynamic_report where type=1 and status=0 order by id desc'
        item = self.db.get_one(sql)
        jid = item[0]
        id = item[1]
        setattr(TestData, 'jid', str(jid))
        setattr(TestData, 'id', str(id))
        sql1 = 'select id,dynamic_comment_id from fybanks_hfjyuan.dynamic_report where type=2 and status=0 order by id desc'
        item1 = self.db.get_one(sql1)
        jid1 = item1[0]
        pid = item1[1]
        setattr(TestData, 'jid1', str(jid1))
        setattr(TestData, 'pid', str(pid))

    @data(*datas)
    def test_dongtaijubaoshenhe(self, case):
        # 准备用例数据
        # 获取url
        base_url = conf.get('hfjyuan', 'url')
        if '#admin_token#' in case['url']:
            case['url'] = case['url'].replace('#admin_token#', conf.get('admin_hfjyuan', 'admin_token'))
        url = base_url + case['url']
        # 获取方法
        method = case['method']
        # 获取data
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])
        # 获取请求头
        headers = eval(case['headers'])
        # 获取期望结果
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        # 发送请求
        response = self.http.send(url=url, method=method, json=data, headers=headers)
        res = response.json()


        # 断言
        try:
            self.assertEqual(expected['state'], res['state'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['interface'] == '动态举报审核' and res['msg']=="":
                sql = replace_data(case['check_sql'])
                status = self.db.get_one(sql)[0]
                self.assertEqual(data['status'], status)
            if case['interface'] == '评论举报审核' and res['msg']=="":
                sql1 = replace_data(case['check_sql'])
                status1 = self.db.get_one(sql1)[0]
                self.assertEqual(data['status'], status1)
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
