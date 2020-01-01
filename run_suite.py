"""
============================
Author  : XiaoLei.Du
Time    : 2019/11/23 17:22
E-mail  : 506615839@qq.com
File    : run_suite.py
============================
"""
import os
import unittest
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.contans import CaseDir, ReportDir, CaseList, BASEDIR
from common.read_conf import conf
from common.mail_send import Email

title = conf.get('report', 'title')
description = conf.get('report', 'description')
tester = conf.get('report', 'tester')


# # 第一步：新建测试套件
# suite = unittest.TestSuite()
# # 第二步：加载测试用例到测试套件
# loader = unittest.TestLoader()
# case_path = os.path.join(CaseDir)
# suite.addTest(loader.discover(case_path))
# # 第三步：新建测试用例启动器
# report_path = os.path.join(ReportDir, 'report.html')
# with open(report_path, 'wb') as f:
#     runner = HTMLTestRunner(
#         stream=f,
#         title=title,
#         description=description,
#         tester=tester
#     )
#     # 第四步：运行用例启动器
#     runner.run(suite)
#     # 测试报告发送
#     mail.send_mail()

class RunCase:
    """获取所有测试用例"""
    def set_case_list(self):
        caseList = []
        fb = open(CaseList)
        for value in fb.readlines():
            data = str(value)
            # 过滤掉不要执行的用例
            if data != '' and not data.startswith("#"):
                caseList.append(data.replace("\n", ""))
        fb.close()
        return caseList

    def set_case_suite(self):
        caseList = self.set_case_list()
        # 创建测试套件
        test_suite = unittest.TestSuite()
        suite_model = []
        # 遍历所有测试用例
        for case in caseList:
            case_file = os.path.join(BASEDIR, "testcases")
            # print(case_file)
            # case_name = case.split("/")[-1]
            # print(case_name + ".py")
            discover = unittest.defaultTestLoader.discover(case_file, pattern=case + '.py', top_level_dir=None)
            suite_model.append(discover)
        # 循环往套件里添加测试用例
        if len(suite_model) > 0:
            for suite in suite_model:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        print(test_suite)
        return test_suite

    def run(self):
        suite = self.set_case_suite()
        report_path = os.path.join(ReportDir, 'report.html')
        with open(report_path, 'wb') as f:
            runner = HTMLTestRunner(
                stream=f,
                title=title,
                description=description,
                tester=tester
            )
        # 第四步：运行用例启动器
            runner.run(suite)
        # 测试报告发送
        emails = Email()
        emails.send_mail()


R = RunCase()
R.run()
