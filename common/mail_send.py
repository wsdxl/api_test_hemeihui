"""
============================
Author  : zhuyuqiang
Time    : 2019/12/09 10:12
E-mail  : zyqkenmy@126.com
File    : mail_send.py
============================
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from common.read_conf import conf
from common.contans import ReportDir
import os

'''
获取最新测试报告
'''
# def get_report():
#     result_dir = contans.ReportDir
#     lists = os.listdir(result_dir)
#     lists.sort(key=lambda fn: os.path.getmtime(result_dir + "\\" + fn) if not
#     os.path.isdir(result_dir + "\\" + fn) else 0)
#     print(u'最新测试生成的报告： ' + lists[-1])
#     # 找到最新生成的文件
#     file_new = os.path.join(result_dir, lists[-1])
#     print(file_new)

class Email:
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = conf.get('EMAIL', 'mail_host')  # SMTP服务器
        self.mail_user = conf.get('EMAIL', 'mail_user')  # 用户名
        self.mail_pass = conf.get('EMAIL', 'mail_pass')  # 密码
        self.sender = conf.get('EMAIL', 'sender')  # 发件人邮箱

    def send_mail(self):
        # 读取测试报告
        report_file = ReportDir + '\\report.html'
        f = open(report_file, 'rb')
        mail_body = f.read()
        receivers = ['542925725@qq.com', 'zyqkenmy@126.com']  # 接收人邮箱
        message = MIMEText(mail_body, 'html', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(receivers)
        # 邮件主题
        message['Subject'] = conf.get('EMAIL', 'Subject')
        port = conf.get('EMAIL', 'mail_port')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, port)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, receivers, message.as_string())  # 发送
            print("测试报告邮件发送成功.")
        except Exception as e:
            print("测试报告邮件发送不成功：")



