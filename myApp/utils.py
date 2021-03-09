from django.core.paginator import Paginator


class CustomPaginator(Paginator):
    def lst(self, page):
        return self.page(page).object_list

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# 自定义发送邮件的函数
'''
配置发邮件所需的基础信息
EMAIL_HOST_USER # 配置发件人邮箱地址
EMAIL_HOST_PASSWORD # 配置发件人邮箱密码
EMAIL_NICK # 配置发件人昵称
to_user # 配置收件人邮箱地址
to_nick # 配置收件人昵称
content # 配置邮件内容
'''


def send_email( tolist, content):
    # 必须将邮件内容做一次MIME的转换 -- 这是发送含链接的邮件
    msg = MIMEText(content, 'html', 'utf-8')
    # 配置发件人名称和邮箱地址
    msg['From'] = formataddr(['zbb', "780357902@qq.com"])
    # 配置邮件主题（标题
    msg['Subject'] = "发送邮件测试"
    # 配置Python与邮件的SMTP服务器的连接通道（如果不是QQ邮箱，SMTP服务器是需要修改的）
    server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=300)
    # 模拟登陆
    server.login("780357902@qq.com",'*******')
    # 邮件内容的发送
    server.sendmail("780357902@qq.com", tolist, msg.as_string())
    # 关闭连接通道
    server.quit()
