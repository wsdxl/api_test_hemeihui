'''
============================
Author  : XiaoLei.Du
Time    : 2019/12/20 10:40
E-mail  : 506615839@qq.com
File    : test_dongtaixiangqing.py
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
class TestDongTaiXiangQing(unittest.TestCase):
    excel=ReadExcel(data_path,'dongtaixiangqing')
    datas=excel.read_excel()
    http=HanderRequest()
    db=HandDB()

    def setUp(self):
        sql='select id  from fybanks_hfjyuan.dynamic_info where status=1 and state=1 order by id desc'
        id=self.db.get_one(sql)[0]
        setattr(TestData,"id",str(id))


    @data(*datas)
    def test_dongtaixiangqing(self,case):
        base_url = conf.get('hfjyuan', 'url')
        if '#admin_token#' in case['url']:
            case['url'] = case['url'].replace('#admin_token#', conf.get('admin_hfjyuan', 'admin_token'))
        url = base_url + case['url']
        print(url)
        method=case['method']
        case['data']=replace_data(case['data'])
        data=eval(case['data'])
        headers=eval(case['headers'])
        expected=eval(case['expected'])
        row=case['case_id']+1

        response=self.http.send(url=url,method=method,params=data,headers=headers)
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

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

if __name__ =="__main__":
    unittest.main()
        

