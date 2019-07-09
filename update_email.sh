#!/bin/sh
#echo >update_email.sh && vim update_email.sh
#bash update_email.sh

#配置蜜罐告警邮件收发
echo "############ 是否配置Opencanary_Web蜜罐邮件收发,输入yes/no?Enter.默认no. ############"
typeset -l select
read select
case $select in
y*)
get_mail_host=`sed -n '30p' /usr/local/src/opencanary_web/application.py |cut -d ' ' -f3`
#30p application.py的第30行正好是配置smtp服务器地址的那行
get_mail_user=`sed -n '31p' /usr/local/src/opencanary_web/application.py |cut -d ' ' -f3`
get_mail_pass=`sed -n '32p' /usr/local/src/opencanary_web/application.py |cut -d ' ' -f3`
get_mail_postfix=`sed -n '33p' /usr/local/src/opencanary_web/application.py |cut -d ' ' -f3`
echo "############正在配置opencanary蜜罐邮件收发###########"
read -p "smtp服务器地址（$get_mail_host）:" mail_host
if [ "$mail_host" = "" ]; then
  echo "$get_mail_host"
   else
  sed -i "s/$get_mail_host/\"$mail_host\"/g" /usr/local/src/opencanary_web/application.py
fi
read -p "邮箱用户名（$get_mail_user）:" mail_user
if [ "$mail_user" = "" ]; then
  echo "$get_mail_user"
   else
  sed -i "s/$get_mail_user/\"$mail_user\"/g" /usr/local/src/opencanary_web/application.py
fi
read -p "输入邮箱密码（$get_mail_pass）:" mail_pass
if [ "$mail_pass" = "" ]; then
  echo "$get_mail_pass"
   else
  sed -i "s/$get_mail_pass/\"$mail_pass\"/g" /usr/local/src/opencanary_web/application.py
fi
read -p "邮箱后缀名（$get_mail_postfix）:" mail_postfix
if [ "$mail_postfix" = "" ]; then
  echo "$get_mail_postfix"
   else
  sed -i "s/$get_mail_postfix/\"$mail_postfix\"/g" /usr/local/src/opencanary_web/application.py
fi
echo "############配置已完成,下一步配置收件人邮箱###########"

get_mail_addressee=`sed -n '2p' /usr/local/src/opencanary_web/util/conf/email.ini | awk '{print $3}'`
read -p "收件人邮箱（$get_mail_addressee）:" mail_addressee
if [ "$mail_addressee" = "" ]; then
  echo "########配置没有做任何更改,默认收件人邮箱:$get_mail_addressee#######"
   else
      sed -i "s/$get_mail_addressee/$mail_addressee/g" /usr/local/src/opencanary_web/util/conf/email.ini
get_new_mail_addressee=`sed -n '2p' /usr/local/src/opencanary_web/util/conf/email.ini | awk '{print $3}'`
      echo "##########已更新告警收件邮箱:$get_new_mail_addressee#########"
fi

mail_switch=`sed -n '3p' /usr/local/src/opencanary_web/util/conf/email.ini |awk '{print $3}'`
if [ "$mail_switch" = "on" ]; then
    echo "#######已开启告警邮件开关########"
    else
    echo "#######正在开启告警邮件开关##########"
    sed -i "s/switch = off/switch = on/g" /usr/local/src/opencanary_web/util/conf/email.ini
    echo "#######开启告警邮件成功##########"
fi
echo "############告警邮件配置已完成############"
echo "############正在重启服务############"
sleep 5
#重启服务配置生效
systemctl restart supervisord.service
systemctl restart nginx.service

#回显已完成
echo "已经配置成功蜜罐告警邮件,具体配置浏览/usr/local/src/opencanary_web/application.py"
echo "收件人邮件配置(以及告警开关):/usr/local/src/opencanary_web/util/conf/email.ini"
echo "更多信息请参考https://github.com/p1r06u3/opencanary_web"
;;
n*)
echo "蜜罐告警邮件没有配置成功,请自行决定是否需要配置."
echo "蜜罐告警具体配置(发件人)浏览/usr/local/src/opencanary_web/application.py"
echo "收件人邮件配置(以及告警开关):/usr/local/src/opencanary_web/util/conf/email.ini"
echo "更多信息请参考https://github.com/p1r06u3/opencanary_web"
;;
*)
echo "蜜罐告警邮件没有配置成功,请自行决定是否需要配置."
echo "蜜罐告警具体配置(发件人)浏览/usr/local/src/opencanary_web/application.py"
echo "收件人邮件配置(以及告警开关):/usr/local/src/opencanary_web/util/conf/email.ini"
echo "更多信息请参考https://github.com/p1r06u3/opencanary_web"
esac
exit 0