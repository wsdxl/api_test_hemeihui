<<<<<<< Updated upstream
"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/23 15:23
E-mail  : 506615839@qq.com
file:   test_pinglun.py
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
=======
import unittest
from common.contans import DataDir
import os
from common.read_conf import conf
from common.paramter_fenzhuang import paramter_fengzhuagn,case_package
from library.ddt import ddt, data
from common.my_logger import my_logger
>>>>>>> Stashed changes

data_path = os.path.join(DataDir, 'shaibaoquan.xlsx')


@ddt
<<<<<<< Updated upstream
class TestPingLun(unittest.TestCase):
    excel = ReadExcel(data_path, 'pinglun')
    datas = excel.read_excel()
    http = HanderRequest()
    db = HandDB()

    @classmethod
    def setUpClass(cls):
        my_login = Login()
        sid, chainRole = my_login.login()
        setattr(TestData, 'sid', sid)

    def setUp(self):
        sql = 'select id from fybanks_hfjyuan.dynamic_info where id not in (select dynamic_id from fybanks_hfjyuan.dynamic_comment where state=1  order by id desc) and status=3 and state=1 order by id desc'
        id = self.db.get_one(sql)[0]
        setattr(TestData, 'id', str(id))

    @data(*datas)
    def test_pinglun(self, case):
        # 获取url地址
        case['url'] = replace_data(case['url'])
        url = conf.get('hfjyuan', 'url') + case['url']
        method = case['method']
        if case['check_sql']:
            item = self.db.get_one(case['check_sql'])
            dynamicId = item[0]
            parentId = item[1]
            topParentId = item[2]
            setattr(TestData, 'dynamicId', str(dynamicId))
            setattr(TestData, 'parentId', str(parentId))
            setattr(TestData, 'topParentId', str(topParentId))
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])
        headers = eval(case['headers'])
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.http.send(url=url, method=method, json=data, headers=headers)
=======
class MyTestCase(unittest.TestCase):
    case_datas = paramter_fengzhuagn(data_path, 'pinglun')

    @data(*case_datas)
    def test_pinglun(self, case):
        # 准备用例数据
        sid = conf.get("hfjyuan", 'sid')
        params=case_package(case,sid)
        # 发送请求
        response = self.http.send(url=params["url"], method=params["method"], json=params["data"],
                                  headers=params["headers"])
>>>>>>> Stashed changes
        res = response.json()

        # 断言
        try:
            self.assertEqual(expected['state'], res['state'])
            self.assertEqual(expected['msg'], res['msg'])
<<<<<<< Updated upstream
            # 评论别人的动态成功，产生一天评论记录
            if case['title'] == '评论别人的动态' and res['msg'] == 'success':
                # sql1 = replace_data(case['check_sql'])
                sql1='select * from fybanks_hfjyuan.dynamic_comment where dynamic_id=89'
                count = self.db.get_count(sql1)
                print(count)
                self.assertEqual(1, count)
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
=======
        except AssertionError as e:
            self.excel.write_excel(row=params["row"], column=11, value='未通过')
            my_logger.info('用例-->{}:执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预期结果：{}".format(params["expected"]))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=params["row"], column=11, value='已通过')
            my_logger.info('用例-->{}:执行已通过'.format(case['title']))
>>>>>>> Stashed changes
