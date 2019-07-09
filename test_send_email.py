#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'domainboy@yeah.net'
receivers = ['sil3nt@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')   # 发送者
message['To'] =  Header("测试", 'utf-8')        # 接收者
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
try:
    server = smtplib.SMTP()
    server.connect('smtp.yeah.net')  #连接服务器
    server.login('domainboy', 'psqtjcbfxtunnwql')  #登录操作
    server.sendmail(sender, receivers, message.as_string())
    server.close()
    print("email send success.")
except Exception as e:
    print("email send failed: " , str(e))
