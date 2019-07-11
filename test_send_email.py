#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import time
import  os

mail_host="smtp.yeah.net"
mail_user="domainboy@yeah.net"
mail_pass="psqtjcbfxtunnwql"
sslPort="465"
time1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

sender = 'domainboy@yeah.net'
to_reciver = ['domainboy@yeah.net']
cc_reciver =[ 'sil3nt@qq.com']
reciver = to_reciver + cc_reciver

message = MIMEText('请管理员尽快处理！！！', _subtype='html', _charset='utf-8')

message['From'] =  sender
message['To'] = ";".join(to_reciver)
message['Cc'] = ";".join(cc_reciver)

subject ='接口自动化报告'+'-'+time1
message['Subject'] = Header(subject, 'utf-8')
"""
try:
    smtpObj = smtplib.SMTP_SSL(mail_host,sslPort)
    smtpObj.ehlo()
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,reciver, message.as_string())
    print ("邮件发送成功")
except Exception as n:
        print ("Error: 无法发送邮件")
        print(n)
exit
"""


me = "opencanary" + "<" + mail_user + "@yeah.net>"
msg = MIMEText('请管理员尽快处理！！！', _subtype='html', _charset='utf-8')
my_email = [mail_user ]
msg['Subject'] = '接口自动化报告'+'-'+time1
msg['From'] = me
msg['To'] = ";".join(my_email)  #将收件人列表以‘;’分隔
msg['Cc'] = ";".join(cc_reciver)
try:
    server = smtplib.SMTP()
    server.connect(mail_host)  #连接服务器
    server.login(mail_user, mail_pass)  #登录操作
    server.sendmail(me, cc_reciver, msg.as_string())
    server.close()
    print("email send success.")
except Exception as e:
    print("email send failed: " , str(e))





"""



#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = ['domainboy@yeah.net']
receivers = ['sil3nt@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('请管理员尽快处理', 'plain', 'utf-8')
message['From'] = Header("domainboy@yeah.net", 'utf-8')   # 发送者
message['To'] =  Header("sil3nt@qq.com", 'utf-8')        # 接收者
message['Cc'] = Header("domainboy@yeah.net", 'utf-8')
subject = '服务器被扫描了'
message['Subject'] = Header(subject, 'utf-8')
 
try:
    server = smtplib.SMTP()
    server.connect('smtp.yeah.net')  #连接服务器
    server.login('domainboy@yeah.net', 'psqtjcbfxtunnwql')  #登录操作
    server.sendmail(sender, sender+receivers, message.as_string())
    server.close()
    print("email send success.")
except Exception as e:
    print("email send failed: " , str(e))
"""