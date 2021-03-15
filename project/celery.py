from __future__ import absolute_import # 绝对路径导入
from celery import Celery
from django.conf import settings
import os

# 设置系统的环境配置用的是Django的
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
# 实例化celery，第一个参数应用名称必须给定
app = Celery('mycelery')
# 设置时区
app.conf.timezone = "Asia/Shanghai"
# 指定celery的配置来源，用的是项目的配置文件settings.py
app.config_from_object('django.conf:settings')
# 让celery自动去发现创建的任务(task)
# 需要在app目录下，新建一个叫tasks.py文件
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))