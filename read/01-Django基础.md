# 01-Django基础

# 
![](https://cdn.nlark.com/yuque/0/2021/jpeg/207655/1612863681013-731e0a62-23b9-4975-a880-8b13aaf6416e.jpeg)# 1 基础
## 1.1 创建项目
### 1.1.1 创建
```shell
django-admin startproject [projectName]
```
### 1.1.2 project目录
![image.png](https://cdn.nlark.com/yuque/0/2021/png/207655/1612759225727-aef01d11-c711-4a10-aae5-8cd12d03b876.png#align=left&display=inline&height=149&margin=%5Bobject%20Object%5D&name=image.png&originHeight=149&originWidth=344&size=9514&status=done&style=none&width=344)

- __init__.py  一个空文件，告诉python这个目录应该被看做一个python包
- settings.py  项目的配置文件
- urls.py  项目的URL声明
- wsgi.py  项目与WSGI兼容的Web服务器入口
- manager.py  一个命令行工具，可以使我们用多种方式对Django项目进行交互
### 1.1.3 配置数据库
注意：Django默认使用SQLite数据库，这里使用Mysql
#### 1.1.3.1 在settings.py文件中，通过DATABASES选项进行数据库配置
#### 1.1.3.2 配置MySQL

- python3.x安装的是PyMySQL
- 在__init__.py文件中写入两行代码
```shell
import pymysql
pymysql.install_as_MySQLdb()
```

- 在settings.py文件中修改数据库配置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306
    }
}
```
### 1.1.4 创建应用
> 一个项目中可以创建多个应用，每个应用进行一种业务处理

在项目下执行，也就是manage.py同级
```shell
python manage.py startapp myApp
```
![image.png](https://cdn.nlark.com/yuque/0/2021/png/207655/1612761502515-3a27621a-f365-44bc-a793-bc055b410b4d.png#align=left&display=inline&height=267&margin=%5Bobject%20Object%5D&name=image.png&originHeight=267&originWidth=206&size=12814&status=done&style=none&width=206)
目录介绍：

- admin.py 站点配置
- models.py 模型
- views.py 视图
### 1.1.5 激活应用

- 在settings.py文件中，将myApp应用加入到INSTALLED_APPS选项中
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myApp'
]
```
### 1.1.6 定义模型

- 概述：有一个数据表，就对应有一个模型
- 在models.py文件中定义模型
- 说明：不需要定义主键，在生成时自动添加，并且值为自动
```python
# 引入
from django.db import models
# 模型类要继承models.Model类
from django.db import models

# Create your models here.
class Grades(models.Model):
    gName = models.CharField(max_length=20)
    gDate = models.DateTimeField()
    gGirlNum = models.IntegerField()
    gBoyNum = models.IntegerField()
    isDelete = models.BooleanField(default=False)


class Students(models.Model):
    sName = models.CharField(max_length=20)
    sGender = models.BooleanField(default=True)
    sAge = models.IntegerField()
    sContEnd = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    # 关联外键
    sGrade = models.ForeignKey("Grades", on_delete=models.CASCADE)

    
```
### 1.1.7 在数据库中生成数据表
#### 1.1.7.1 生成迁移文件
在manage.py同级执行
```bash
# 创建迁移文件
python manage.py makemigrations
```
![image.png](https://cdn.nlark.com/yuque/0/2021/png/207655/1612763121282-e73dfe03-9405-4bff-a735-7925b7d214b4.png#align=left&display=inline&height=200&margin=%5Bobject%20Object%5D&name=image.png&originHeight=200&originWidth=178&size=8145&status=done&style=none&width=178)
#### 1.1.7.2 生成数据库表
```bash
python manage.py migrate
```
![image.png](https://cdn.nlark.com/yuque/0/2021/png/207655/1612763423136-1ce5f973-c1cc-47f4-ad98-aeee71bcd8db.png#align=left&display=inline&height=272&margin=%5Bobject%20Object%5D&name=image.png&originHeight=272&originWidth=269&size=13932&status=done&style=none&width=269)
### 1.1.8 测试数据库操作
#### 1.1.8.1 进入到python shell
```bash
python manage.py shell
```
#### 1.1.8.2 引入包
```bash
from myApp.models import Grades,Students
from django.utils import timezone
from datetime import *
```
#### 1.1.8.3 操作数据

- 查询所有数据
```bash
# 类型.objects.all() 通过模型类去查询数据库
Grades.objects.all()
```

- 添加数据
```bash
# 本质：创建一个模型类的对象实例
grade1 = Grades()
grade1.gName = "py"
grade1.gDate = datetime(year=2021,month=1,day=1)
grade1.gGirlNum = 3
grade1.gBoyNum = 10
grade1.save()
```
再次查询
```bash
>>> Grades.objects.all()
<QuerySet [<Grades: Grades object (1)>]>
# 这样看起来很不直观，直接可以在models.py中写入
class Grades(models.Model):
    gName = models.CharField(max_length=20)
    gDate = models.DateTimeField()
    gGirlNum = models.IntegerField()
    gBoyNum = models.IntegerField()
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return "%s-%d-%d" % (self.gName, self.gGirlNum, self.gBoyNum)
```
重新进入终端再次查询
```bash
from myApp.models import Grades,Students
from django.utils import timezone
from datetime import *
Grades.objects.all()

>>> Grades.objects.all()
<QuerySet [<Grades: py-3-10>]>

```

- 查询单条数据
```bash
# 类.objects.get(pk=2)
Grades.objects.get(pk=2)
```

- 修改数据
```bash
# 模型对象.属性 = 新值
grade2 = Grades.objects.get(pk=2)
grade2.gBoyNum = 222
grade2.save()
```

- 删除数据
```bash
# 模型对象.delete()
grade2.delete()
# 注意：物理删除，数据库中数据将真实被删除
```

- 关联对象
```bash
grade1 = Grades.objects.get(pk=1)
stu1 = Students()
stu1.sName = 'zhangsan'
stu1.sGender = False
stu1.sAge = 20
stu1.sContEnd = "test"
stu1.sGrade = grade1
stu1.save()
```
![image.png](https://cdn.nlark.com/yuque/0/2021/png/207655/1612765533756-805deeba-a56a-4e56-abc0-173682d0da41.png#align=left&display=inline&height=98&margin=%5Bobject%20Object%5D&name=image.png&originHeight=98&originWidth=804&size=11124&status=done&style=none&width=804)

   - 获取关联对象的集合
```bash
# 获取某班级所有学生 对象.关联的类名小写_set.all()
# 1.获取指定班级，获取班级下所有关联的学生
grade1 = Grades.objects.get(pk=1)
grade1.students_set.all()
```

   - 创建并关联
```bash
grade1 = Grades.objects.get(pk=1)
stu3 = grade1.students_set.create(sName=u'xxx',sGender=True,sContEnd=u'zzz',sAge=20)

```
### 1.1.9 启动服务器
> 这是一个纯python写的轻量级web服务器，仅仅在开发测试中使用

```bash
# ip:port可以不写，不写默认代表本机ip，端口号默认8000
python manage.py runserver ip:port

```
### 1.1.10 Admin站点管理
> 概述：
> - 内容发布：负责增删改内容
> - 


1. 配置Admin应用

settings.py
```bash
# 配置Admin应用，默认已添加
INSTALLED_APPS = [
    'django.contrib.admin', 配置Admin应用
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myApp'
]
```

2. 创建管理员用户
```bash
# 依次输入用户名 密码 邮箱
python manage.py createsuperuser
```

3. 汉化
> 登录[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

修改settings.py 中 LANGUAGE_CODE = 'en-us'
```bash
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'
```

4. 管理数据表

修改admin.py后刷新界面
```bash
from django.contrib import admin

# Register your models here.
from .models import Grades, Students

# 注册
admin.site.register(Grades)
admin.site.register(Students)

```

5. 自定义管理页面
> 依旧是修改admin.py，其中主要六个属性
> 布尔值显示问题
> 设置页面列的名称
> 执行动作的位置

```bash
from django.contrib import admin

# Register your models here.
from .models import Grades, Students


# 注册
class StudentsInfo(admin.TabularInline):
    model = Students
    extra = 2

class GradesAdmin(admin.ModelAdmin):
    inlines = [StudentsInfo]
    # 列表列属性
    # 显示字段
    list_display = ['pk', 'gName', 'gDate', 'gGirlNum', 'gBoyNum', 'isDelete']
    # 过滤字段
    list_filter = ['gName', 'gDate']
    # 搜索字段
    search_fields = ['gName']
    # 分页
    list_per_page = 10

    # 添加、修改页属性，fields和fieldsets不能同时使用
    # 规定属性的先后顺序
    # fields = ['gName', 'gGirlNum', 'gBoyNum', 'isDelete', 'gDate']
    # 给属性分组
    fieldsets = [
        ("num", {"fields": ['gGirlNum', 'gBoyNum']}),
        ("base", {"fields": ['gName', 'gDate', 'isDelete']}),
    ]
    # 创建班级时添加student

admin.site.register(Grades, GradesAdmin)

class StudentsAdmin(admin.ModelAdmin):
    # 布尔值显示问题
    def gender(self):
        if self.sGender:
            return '男'
        else:
            return '女'
        # 设置页面列名称

    gender.short_description = '性别'

    list_display = ['pk', 'sName', 'sAge', gender, 'sContEnd', 'sGrade', 'isDelete']
    list_per_page = 10


admin.site.register(Students, StudentsAdmin)

```

6. 使用装饰器来注册
```bash
@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
	pass
# admin.site.register(Students, StudentsAdmin)
```
### 1.1.11 视图的基本使用
#### 概述
> 在Django中，视图对web请求进行回应
> 视图就是一个python函数，在views.py文件中定义

#### 定义视图
views.py
```bash
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("hello world")

```
#### 配置url
修改project目录下的urls.py文件
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myApp.urls'))
]
```
在myApp目录下创建urls.py文件
```bash
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^(\d+)$', views.details),
]

```
访问[http://127.0.0.1:8000/](http://127.0.0.1:8000/)则显示内容
### 1.1.12 模板的基本使用
#### 概述
> 模板是HTML页面，可以根据视图中传递过来的数据进行填充

#### 创建模板目录
创建templates目录，在目录下创建对应项目的模板目录(project/templates/myApp)
#### 配置模板路径
修改settings.py文件下TEMPLATES
```bash
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
#### 新建project/templates/myApp/grades.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>班级信息</title>
</head>
<body>
<h1>班级信息列表</h1>
<ul>
    {% for grade in grades %}
        <li>
            <a href="#">{{grade.gName}}</a>
        </li>
    {% endfor %}
</ul>
</body>
</html>
```
#### 配置urls.py views.py
```html
# urls.py 增加匹配
re_path(r'^grades/$',views.grades)
# views.py 增加
def grades(request):
    # 去模板取数据
    gradesList = Grades.objects.all()
    # 将数据传递给模板，模板再渲染页面，将渲染好的页面返回给浏览器
    return render(request, 'myApp/grades.html', {"grades": gradesList})
```
#### 浏览器访问[http://127.0.0.1:8000/grades/](http://127.0.0.1:8000/grades/)


