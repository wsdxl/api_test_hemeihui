'''
============================
Author  : XiaoLei.Du
Time    : 2019/12/19 14:40
E-mail  : 506615839@qq.com
File    : test_guanzhuyonghu.py
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

data_path=os.path.join(DataDir,'shaibaoquan.xlsx')

@ddt
class TestGuanZhuYongHu(unittest.TestCase):
    excel=ReadExcel(data_path,'guanzhuyonghu')
    datas=excel.read_excel()
    http=HanderRequest()

    @classmethod
    def setUpClass(cls):
        my_login = Login()
        sid, chainRole = my_login.login()
        setattr(TestData, 'sid', sid)


    @data(*datas)
    def test_guanzhuyonghu(self,case):
        # 准备用例数据
        url=conf.get('hfjyuan','url')+case['url']
        method=case['method']
        case['data']=replace_data(case['data'])
        data=eval(case['data'])
        headers=eval(case['headers'])
        expected=eval(case['expected'])
        row=case['case_id']+1
        # 请求数据
        response=self.http.send(url=url,method=method,data=data,headers=headers)
        res=response.json()

        # 断言
        try:
            self.assertEqual(expected['state'],res['state'])
            self.assertEqual(expected['msg'], res['msg'])
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



