'''
============================
Author  : XiaoLei.Du
Time    : 2019/12/13 16:08
E-mail  : 506615839@qq.com
File    : test_fabu.py
============================
'''
import os
import unittest
from library.ddt import ddt,data
from common.read_excel import ReadExcel
from common.contans import DataDir
from common.login import Login
from common.hander_data import TestData,replace_data
from common.hander_request import HanderRequest
from common.read_conf import conf
from common.my_logger import my_logger
from common.hande_db import HandDB

data_path=os.path.join(DataDir,'shaibaoquan.xlsx')

@ddt
class TestFaBu(unittest.TestCase):
    excel=ReadExcel(data_path,'dongtaifabu')
    add_data=excel.read_excel()
    http=HanderRequest()
    db=HandDB()


    @classmethod
    def setUpClass(cls):
        my_login = Login()
        sid, chainRole = my_login.login()
        setattr(TestData, 'sid', sid)
        setattr(TestData,'chainRole',chainRole)

    @data(*add_data)
    def test_fabu(self,case):
        # 准备用例数据
        case['url'] = replace_data(case['url'])
        url=conf.get('hfjyuan','url')+case['url']

        method=case['method']
        data=eval(case['data'])
        expected=eval(case['expected'])

        headers=eval(case['headers'])
        row=case['case_id']+1
        if case['check_sql']:
            sql = replace_data(case['check_sql'])
            before_count = self.db.get_count(sql)

        # 发送请求
        response=self.http.send(url=url,method=method,json=data,headers=headers)
        res=response.json()

        # 断言
        try:
            self.assertEqual(expected['state'],res['state'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['check_sql']:
                sql = replace_data(case['check_sql'])
                after_count=self.db.get_count(sql)
                self.assertEqual(1,after_count-before_count)

        except AssertionError as e:
            self.excel.write_excel(row=row, column=11, value='未通过')
            my_logger.info('用例-->{}:执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=row,column=11,value='已通过')
            my_logger.info('用例-->{}:执行已通过'.format(case['title']))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()



if __name__ =='__main__':
    unittest.main()