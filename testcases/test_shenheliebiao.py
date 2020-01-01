'''
============================
Author  : XiaoLei.Du
Time    : 2019/12/20 9:22
E-mail  : 506615839@qq.com
File    : test_delete_dongtai.py
============================
'''
import os
import unittest
from library.ddt import ddt,data
from common.contans import DataDir
from common.read_excel import ReadExcel
from common.read_conf import conf
from common.hander_data import TestData,replace_data
from common.hander_request import HanderRequest
from common.my_logger import my_logger

data_path=os.path.join(DataDir,'shaibaoquan.xlsx')

@ddt
class TestShenHeLieBiao(unittest.TestCase):
    excel=ReadExcel(data_path,'shenheliebiao')
    datas=excel.read_excel()
    http=HanderRequest()



    @data(*datas)
    def test_shenheliebiao(self,case):
        # 准备用例数据
        # 获取url
        base_url = conf.get('hfjyuan', 'url')
        if '#admin_token#' in case['url']:
            case['url'] = case['url'].replace('#admin_token#', conf.get('admin_hfjyuan', 'admin_token'))
        url = base_url + case['url']
        # 获取方法
        method=case['method']
        # 获取data
        data=eval(case['data'])
        # 获取请求头
        headers=eval(case['headers'])
        # 获取期望结果
        expected=eval(case['expected'])
        row=case['case_id']+1

        # 发送请求
        response=self.http.send(url=url,method=method,json=data,headers=headers)
        res=response.json()

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