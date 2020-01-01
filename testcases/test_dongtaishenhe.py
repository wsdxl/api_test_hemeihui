'''
============================
Author  : XiaoLei.Du
Time    : 2019/12/16 14:51
E-mail  : 506615839@qq.com
File    : test_shenhe.py
============================
'''
import unittest
import os
from common.read_excel import ReadExcel
from common.contans import DataDir
from library.ddt import ddt, data
from common.hander_data import TestData, replace_data
from common.login import Login
from common.read_conf import conf
from common.hander_request import HanderRequest
from common.hande_db import HandDB
from common.my_logger import my_logger

data_path = os.path.join(DataDir, 'shaibaoquan.xlsx')


@ddt
class TestShenHe(unittest.TestCase):
    excel = ReadExcel(data_path, 'dongtaishenhe')
    shenhe_data = excel.read_excel()
    http = HanderRequest()
    db = HandDB()

    @classmethod
    def setUpClass(cls):
        my_login = Login()
        sid, chainRole = my_login.login()
        setattr(TestData, 'sid', sid)
        setattr(TestData, 'chainRole', chainRole)

    def setUp(self):
        fabu_url = '/circle-api/m/circle/dynamic-info/save?sid=' + getattr(TestData, 'sid')
        url = conf.get('hfjyuan', 'url') + fabu_url
        data = {
            "title": "我爱晒宝圈",
            "detail": "我的宝贝超级好",
            "type": 1,
            "status": 1,
            "viewList": [
                {
                    "imgUrl": "https://img.alicdn.com/tfs/TB1MaxEmcLJ8KJjy0FnXXcFDpXa-884-884.jpg",
                    "width": "200px",
                    "height": "300px",
                    "productList": [
                        {
                            "title": "测试商品1号",
                            "xAxis": "112.11",
                            "yAxis": "113.11",
                            "productId": 50,
                            "style": "esse ut et"
                        }
                    ]
                }
            ],
            "labelList": [
                {
                    "labelName": "品牌魅族"
                }
            ]
        }
        headers = {"Content-Type": "application/json"}
        response = self.http.send(url=url, method='post', json=data, headers=headers)
        res = response.json()
        # 获取数据库中新增的发布id
        sql = 'select id from fybanks_hfjyuan.dynamic_info where user_id=69301  order by id desc'
        id = self.db.get_one(sql)[0]
        setattr(TestData, 'id', str(id))

    @data(*shenhe_data)
    def test_shenhe(self, case):
        # 准备用例数据
        # 获取url地址
        base_url = conf.get('hfjyuan', 'url')
        if '#admin_token#' in case['url']:
            case['url'] = case['url'].replace('#admin_token#', conf.get('admin_hfjyuan', 'admin_token'))
        url = base_url + case['url']
        print(url)
        # 获取方法
        method = case['method']
        # 获取data
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])
        # 获取 headers值
        headers = eval(case['headers'])
        # 获取期望结果
        expected = eval(case['expected'])
        # 获取row
        row = case['case_id'] + 1

        # 发送请求
        response = self.http.send(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 断言
        try:
            self.assertEqual(expected['state'], res['state'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['title'] == '审核通过':
                sql = replace_data(case['check_sql'])
                id = self.db.get_one(sql)[0]
                status = self.db.get_one(sql)[1]
                setattr(TestData, 'pass_id', str(id))
                self.assertEqual(3, status)
            if case['title'] == '审核不通过':
                sql = replace_data(case['check_sql'])
                status = self.db.get_one(sql)[1]
                self.assertEqual(2, status)
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


if __name__ == '__main__':
    unittest.main()
