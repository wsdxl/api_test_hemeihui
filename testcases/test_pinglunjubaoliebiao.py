"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/23 14:55
E-mail  : 506615839@qq.com
file:   test_pinglunjubaoliebiao.py
============================
"""
import unittest
import os
from library.ddt import ddt,data
from common.read_excel import ReadExcel
from common.contans import DataDir
from common.read_conf import conf
from common.hander_request import HanderRequest
from common.my_logger import my_logger


data_path=os.path.join(DataDir,'shaibaoquan.xlsx')

@ddt
class TestPingLunJuBaoLieBiao(unittest.TestCase):
    excel=ReadExcel(data_path,'pinglunjubaoliebiao')
    datas=excel.read_excel()
    http=HanderRequest()

    @data(*datas)
    def test_pinglunjubaoliebiao(self,case):
        # 获取url地址
        base_url = conf.get('hfjyuan', 'url')
        if '#admin_token#' in case['url']:
            case['url'] = case['url'].replace('#admin_token#', conf.get('admin_hfjyuan', 'admin_token'))
        url = base_url + case['url']
        method=case['method']
        data=eval(case['data'])
        headers=eval(case['headers'])
        expected=eval(case['expected'])
        row=case['case_id']+1

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

