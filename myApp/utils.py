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


def send_email(tolist, content):
    # 必须将邮件内容做一次MIME的转换 -- 这是发送含链接的邮件
    msg = MIMEText(content, 'html', 'utf-8')
    # 配置发件人名称和邮箱地址
    msg['From'] = formataddr(['zbb', "780357902@qq.com"])
    # 配置邮件主题（标题
    msg['Subject'] = "发送邮件测试"
    # 配置Python与邮件的SMTP服务器的连接通道（如果不是QQ邮箱，SMTP服务器是需要修改的）
    server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=300)
    # 模拟登陆
    server.login("780357902@qq.com", '*******')
    # 邮件内容的发送
    server.sendmail("780357902@qq.com", tolist, msg.as_string())
    # 关闭连接通道
    server.quit()


import os
from datetime import datetime
from random import randint


class FileUpload:
    def __init__(self, file, exts=['png', 'jpg', 'jpeg'], size=1024 * 1024, is_random_name=False):
        """
        :param file: 文件上传对象
        :param exts: 文件类型
        :param size: 文件大小，默认1M
        :param is_random_name: 是否是随机文件夹，默认是否
        """
        self.file = file
        self.exts = exts
        self.size = size
        self.is_random_name = is_random_name

    # 文件上传
    def upload(self, dest):
        """

        :param dest: 文件上传的目标目录
        :return:
        """
        # 1. 判断文件类型是否匹配
        if not self.check_type():
            return -1
        # 2. 判断文件大小是否符合要求
        if not self.check_size():
            return -2
        # 3. 如果是随机文件名，生成随机文件名
        if self.is_random_name:
            self.file_name = self.random_filename()
        else:
            self.file_name = self.file.name
        # 4. 拼接目标文件路径
        path = os.path.join(dest, self.file_name)
        # 5. 保存文件
        self.write_file(path)
        return 1

    def check_type(self):
        ext = os.path.splitext(self.file.name)  # 获取文件后缀
        print(ext, 'ext')
        if len(ext) > 1:
            ext = ext[1].lstrip(".")
            if ext in self.exts:
                return True
        return False

    def check_size(self):
        if self.size < 0:
            return False
        # 如果文件大小给定大小，返回True，否则返回False
        return self.file.size <= self.size

    def random_filename(self):
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(randint(1, 10000))
        ext = os.path.splitext(self.file.name)
        print(ext, 'ext')
        # 获取文件后缀
        ext = ext[1] if len(ext) > 1 else ''
        filename += ext
        return filename

    def write_file(self, path):
        with open(path, 'wb') as fp:
            if self.file.multiple_chunks():
                for chunk in self.file.chunks():
                    fp.write(chunk)
            else:
                fp.write(self.file.read())
