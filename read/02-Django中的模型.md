# 02-Django中的模型

![](https://cdn.nlark.com/yuque/0/2021/jpeg/207655/1613187799305-5f8a509b-e442-4317-a5e2-d9d10596ad95.jpeg)# 1 定义属性
## 概述

- Django根据属性的类型确定以下信息
   - 当前选择的数据库支持字段的类型    
   - 渲染管理表单时使用的默认Html控件
   - 在管理站点最低限度的验证
- 属性命名限制
   - 不能是Python保留关键字
   - 由于Django的查询方式，不允许使用连续的下划线
## 库

- 定义属性时，需要字段类型，字段类型被定义在django.db.models.fields目录下，为了方便使用，被导入到django.db.models中
- 使用方式
   - 导入from django.db import models
   - 通过models.Field创建字段类型的对象，赋值给属性
## 逻辑删除

- 对于重要数据都做逻辑删除，不做物理删除，定义方法是定义isDelete属性，类型为BooleanField，默认值为False
## 字段类型

- AutoField
   - 一个根据实际ID自动增长的IntegerField，通常不指定
   - 一个主键字段将自动添加到模型中
- CharField(max_length=20)
   - 字符串，默认表单样式是TextInput
- TextField
   - 大文本字段，一般超过4000使用，默认的表单控件是Textarea
- IntegerField
   - 整数
- DecimalField(max_digits=None,decimal_places=None)
   - 使用python的Decimal实例表示的十进制浮点数
   - 参数说明
      - DecimalField.max_digits
         - 位数总数
      - DecimalField.decimal_places
         - 小数点后的数字位数
- FloatField
   - 用Python的float实例来表示的浮点数
- BooleanField
   - true/false字段，此字段的默认表单控制是CheckboxInput
- NullBooleanField
   - 支持null/true/false三种值
- DateField[auto_now=False,auto_now_add=False]
   - 使用Python的datetime.date实例表示的日期
   - 参数说明
      - DateField.auto_now
         - 每次保存对象时，自动设置该字段为当前时间，用于最后一次修改的时间戳，总是使用当前日期，默认为false
      - DateField.auto_now_add
         - 当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为False
   - 说明
      - 该字段默认对应的表单控件是一个TextInput，在管理原站点添加一个JavaScript写的日历控件，和一个Today的快捷按钮， 包含一个额外的Invalid_date错误消息键
   - 注意
      - auto_now_add,auto_now,and default 这些设置是相互排斥的，它们之间的任何组合将会发生错误的结果
- TimeField
   - 使用Python的datetime.time实例表示的时间，参数同DateField
- DateTimeField
   - 使用python的datetime.datetime实例表示的日期和时间，参数同DateField
- FileField
   - 一个上传文件的字段
- ImageField
   - 继承了FileField的所有属性和方法，但对上传的对象进行校验，确保它是个有效的image
## 字段选项

- 概述
   - 通过字段选项，可以实现对字段的约束
   - 在字段对象，通过关键字参数指定
- null
   - 如果为True，Django将空值以NULL存储到数据库中，默认值是False
- blanke
   - 如果为True，则该字段允许为空白，默认值是False
- null是数据库范畴的概念，blank是表单验证范畴
- db_column
   - 字段的名称，如果未指定，则使用属性的名称
- db_index
   - 若值为True，则在表单中会为此字段创建索引
- default
   - 默认值
- primary_key
   - 若为True，则该字段会成为模型的主键字段
- unique
   - 如果为True，这个字段在表中必须为唯一值
## 关系

- 分类
   - ForeignKey 一对多，将字段定义在多的端中
   - ManyToManyField 多对多，将字段定义在两端中
   - OneToOneField 一对一，将字段定义在任意一端中
- 用一访问多
   - 格式
      - 对象.模型类小写_set
   - 示例
      - grade.students_set
- 用一访问一
   - 格式
      - 对象.模型类小写
   - 示例
      - grade.students
- 访问id
   - 格式
      - 对象.属性_id
   - 示例
      - students.sgrade_id
## 元选项
在模型类中定义Meta类，用于设置元信息
```bash
class Students(models.Model):
    sName = models.CharField(max_length=20)
    sGender = models.BooleanField(default=True)
    sAge = models.IntegerField()
    sContEnd = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    # 关联外键
    sGrade = models.ForeignKey("Grades", on_delete=models.CASCADE)

    def __str__(self):
        return self.sName

    class Meta:
        db_table = "students"
        ordering = ['-id']
```

- db_table
   - 定义数据库表名，推荐使用小写字母，数据表明默认为项目名小写_类名小写
- ordering
   - 对象的默认排序字段，获取对象的列表时使用
   - 升序 ordering = ['id']
   - 降序 ordering = ['-id']
## 模型成员
### 类属性
#### objects

- 是Manager类型的一个对象，作用是与数据库进行交互
- 当定义模型类是没有指定管理器，则Django为模型创建一个名为objects的管理器
#### 自定义管理器
```bash
class Students(models.Model):
    # 自定义模型管理器
    # 当自定义模型管理器，objects就不存在了
    stuObj = models.Manager()
```

- 当为模型指定管理器，Django就不在为模型类生成objects模型管理器
#### 自定义管理器Manager类

- 模型管理器是Django的模型进行与数据库进行交互的接口，一个模型可以有多个管理器
- 作用
   - 向管理器类中添加额外的方法
   - 修改管理器返回的原始查询集
```bash
class StudentsManager(models.Manager):
    def get_queryset(self):
        return super(StudentsManager,self).get_queryset() \
            .filter(isDelete=False)


class Students(models.Model):
    # 自定义模型管理器
    # 当自定义模型管理器，objects就不存在了
    stuObj = models.Manager()
    stuObj2 = StudentsManager()

// python shell
>>> from myApp.models import Students
>>> Students.objects.all()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: type object 'Students' has no attribute 'objects'
>>> Students.stuObj.all()
<QuerySet [<Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>]>
>>> Students.stuObj2.all()
<QuerySet [<Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>, <Students: zzz>]>

```
### 创建对象

- 目的：向数据库中添加数据
- 当创建对象时，django不会对数据库进行读写操作，当调用save()方式时才与数据库交互，将对象保存到数据库表中
- 注意：__init__方法已经在父类models.Model中使用，在自定义的模型中无法使用
- 方法：
   - 在模型类中增加一个类方法
   - 

```bash
# 在模型类中增加一个类方法
class Students(models.Model):
    # 定义一个类方法创建对象
    @classmethod
    def createStudent(cls, name, age, gender, content, grade, lastTime, isDelete=False):
        stu = cls(sName=name, sAge=age, sGender=gender, sContEnd=content, lastTime=lastTime, isDelete=isDelete,
                  sGrade=grade)
        return stu

# 在定义管理器中添加一个方法
class StudentsManager(models.Manager):
    def get_queryset(self):
        return super(StudentsManager, self).get_queryset() \
            .filter(isDelete=False)

    def createStudent(self, name, age, gender, content, grade, lastTime, isDelete=False):
        stu = self.model()
        stu.sName = name
        stu.sAge = age
        stu.sGender = gender
        stu.sContEnd = content
        stu.sGrade = grade
        stu.lastTime = lastTime
        return stu

```
## 模型查询
### 概述

- 查询集表示从数据库获取的对象集合
- 查询集可以有多个过滤器
- 过滤器就是一个函数，基于所给的参数限制查询集结果
- 从sql角度来说，查询集合select语句等价，过滤器就像where条件
### 查询集

- 在管理器上调用过滤器方法返回查询集
- 查询集经过过滤器筛选后返回新的查询集，所以可以写成链式调用
- 惰性执行  创建查询集不会带来任何数据的访问，直到调用数据时，才会访问数据
- 直接访问数据的情况  ： 迭代、序列化、与if合用
- 返回查询集的方法称为过滤器
   - all() 返回查询集中的所有数据
   - filter() 返回符合条件的数据 filter(key=value) filter(key=value,key=value) filter(key=value).filter(key=value)
   - exclude() 过滤掉符合条件的数据
   - order_by() 排序
   - values() 一条数据就是一个对象(字典），返回一个列表
- 返回单个数据
   - get()    返回一个满足条件的对象    
      - 注意：如果没有找到符合条件的对象，模型类会引发异常"模型类.DoesNotExist"异常
      - 如果找到多个对象，模型类会引发异常"模型类.MultipleObjectsReturned"异常
   - count()    返回查询集的个数
   - first()    返回查询集中第一个对象
   - last()    返回查询集中最后一个对象
   - exists()    判断查询集中是否有对象，有则返回True
```bash
class StudentsManager(models.Manager):
    def get_queryset(self):
        return super(StudentsManager, self).get_queryset() \
            .filter(isDelete=False)
```

- 限制查询集
   - 查询集返回列表，可以使用下标的方法进行限制，等同于sql中的limit语句
   - 注意：下标不能是负数
```bash
# views.py
# 分页
def students(request, page):
    # 去模板取数据
    page = int(page)
    studentsList = Students.stuObj.all()[(page - 1) * 5:page * 5]
    # 将数据传递给模板，模板再渲染页面，将渲染好的页面返回给浏览器
    return render(request, 'myApp/students.html', {"students": studentsList})

```

- 查询集的缓存
   - 概述：每个查询集都包含一个缓存，来最小化的对数据库访问
   - 在新建的查询集中，缓存首次为空，第一次对查询集求值，会发生数据缓存，django会将查询出来的数据做一个缓存，并返回查询结构，以后的查询直接使用查询集的缓存
- 字段查询
   - 概述：
      - 实现sql中的where语句，作为方法filter()、exclude()、get()的参数
      - 语法    属性名称__比较运算符=值
      - 外键    属性名_id
      - 转义    类似SQL中的like语句，like语句中使用%是为了匹配占位，匹配数据中的%(where like '\%')    filter(sName__contains='%')
   - 比较运算符
      - exact    判断，大小写敏感  filter(isDelete=False)
      - contains    是否包含，大小敏感    Students.stuObj.filter(sName__contains="xxx")
      - startswith、endswith     以value开头或结尾，大小写敏感
      - 以上四个在前面加上i，就表示不区分大小写iexact、icontains、istartswith、iendswith
      - isnull、isnotnull    是否为空    filter(sName__isnull=False)
      - in    是否包含在范围内
      - gt 大于    gte 大于等于    lt小于    lte小于等于
      - year  month  day week_day hour minute second
      - 跨关联查询
         - 处理join查询    语法    模型类名__属性名__比较运算符
         - Grades.objects.filter(students__sContend__contains='xxx') 过滤出描述为xxx的班级
      - 查询快捷    pk    代表的主键
   - 聚合函数   
      - 使用aggregate()函数返回聚合函数的值    from django.db.models import Max
         - Avg 
         - Count
         - Max    maxAge=Students.stuObj.aggregate(Max('sAge'))
         - Min
         - Sum
   - F对象    from django.db.models import F,Q
      - 可以使用模型的A属性与B属性进行比较
         - Grades.objects.filter(gGirlNum__gt=F('gBoyNum'))
      - 支持F对象的算术运算
         - Grades.objects.filter(gGirlNum__gt=F('gBoyNum')+20）
   - Q对象
      - 概述：过滤器的方法中的关键字参数，条件为And模式
      - 需求    进行or查询
      - 解决    使用Q对象
         - Students.stuObj.filter(Q(pk__lte=3)|Q(sAge__gt=50))
         - Students.stuObj.filter(Q(pk__lte=3))  只有一个Q对象，就是用于匹配
         - Students.stuObj.filter(~Q(pk__lte=3)) ~取反
