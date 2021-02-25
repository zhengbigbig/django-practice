from django.db import models


# Create your models here.

class Grades(models.Model):
    gName = models.CharField(max_length=20)
    gDate = models.DateTimeField()
    gGirlNum = models.IntegerField()
    gBoyNum = models.IntegerField()
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.gName

    class Meta:
        db_table = "grades"


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


class Students(models.Model):
    # 定义一个类方法创建对象
    @classmethod
    def createStudent(cls, name, age, gender, content, grade, lastTime, isDelete=False):
        stu = cls(sName=name, sAge=age, sGender=gender, sContEnd=content, lastTime=lastTime, isDelete=isDelete,
                  sGrade=grade)
        return stu

    # 自定义模型管理器
    # 当自定义模型管理器，objects就不存在了
    stuObj = models.Manager()
    stuObj2 = StudentsManager()

    sName = models.CharField(max_length=20)
    sGender = models.BooleanField(default=True)
    sAge = models.IntegerField()
    sContEnd = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    # 关联外键
    sGrade = models.ForeignKey("Grades", on_delete=models.CASCADE)

    def __str__(self):
        return self.sName

    lastTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "students"
        ordering = ['-id']


from tinymce.models import HTMLField


class Text(models.Model):
    str = HTMLField()


class BlogsPost(models.Model):
    title = models.CharField(max_length=150)
    # body = models.TextField()
    body = HTMLField()  # 注册
    timestamp = models.DateTimeField()
    auth = models.TextField(default='鲁迅')
    address = models.CharField(max_length=100, default='北京')
