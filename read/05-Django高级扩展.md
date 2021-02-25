# 05-Django高级扩展

![](https://cdn.nlark.com/yuque/0/2021/jpeg/207655/1614245404154-df336e0d-fbc1-41e8-a39e-3ac9b2ca7722.jpeg)# 上传图片
## 代码示例
### upload.html
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form method="post" action="/savefile/" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="file">
    <input type="submit" value="上传">
</form>
</body>
</html>
```
### myApp/urls.py
```bash
    re_path(r'^upload/$', views.upload),
    re_path(r'^savefile/$', views.savefile),
```
### myApp/views.py
```bash
def upload(request):
    return render(request, 'myApp/upload.html')


from django.conf import settings


def savefile(request):
    if request.method == 'POST':
        f = request.FILES['file']
        print(f)
        filePath = os.path.join(settings.MEDIA_ROOT, f.name)
        with open(filePath, 'wb') as fp:
            for info in f.chunks():
                fp.write(info)
        return HttpResponse('上传成功')
    else:
        return HttpResponse("上传失败")
```
# 分页
## 分页代码
### myApp/views.py
```bash
def studentpage(request):
    page = request.GET.get('current', 1)
    pageSize = request.GET.get('pageSize', 10)
    allList = Students.objects.all()
    paginator = Paginator(allList, pageSize)
    currentPageList = paginator.page(page)

    return render(request, 'myApp/studentpage.html', {"students": currentPageList})
```
# celery
> [http://docs.jinkan.org/docs/celery/](http://docs.jinkan.org/docs/celery/)

### 问题

- 用户发起request，并且要等待response返回，但是在视图中又一些耗时的操作，导致用户可能会等待很长时间才能接受response，这样用户体验很差
- 网站每隔一段时间要同步一次数据，但是http请求是需要触发的
### 解决

- celery解决
   - 将耗时的操作放到celery执行
   - 使用celery定时执行
### celery

- 任务
   - 本质是一个python函数，将耗时操作封装成一个函数
- 队列    
   - 将要执行的任务放队列里
- 工人   
   - 负责执行队列中的任务
- 代理
   - 负责调度，在部署环境中使用redis
### 安装

- pip install celery
- pip install celery-with-redis
- pip install django-celery
### 配置
#### settings.py
```bash
INSTALLED_APPS = [
		...
    'djcelery',
]

# celery
import djcelery

djcelery.setup_loader()  # 初始化
BROKER_URL = 'redis://:test@127.0.0.1:6379/0'
CELERY_IMPORTS = ('myApp.task')
```
#### 创建project/myApp/task.py
#### 迁移，生成celery需要的数据库表
```bash
python manage.py migrate
```
#### project/celery.py
```bash
from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

from django.conf import settings  # noqa

app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```
#### 在工程目录下的__init__.py文件中添加
```bash
from .celery import app as celery_app
```


