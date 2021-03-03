from django.db import models


class Student(models.Model):
    sno = models.CharField(max_length=6, primary_key=True)
    sname = models.CharField(max_length=100, null=False)
    ssex = models.CharField(max_length=2, default='男', null=True)
    sage = models.IntegerField(null=True)
    sclass = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'student'


class Archives(models.Model):
    idcard = models.CharField(max_length=18, unique=True)
    address = models.CharField(max_length=200, null=True)
    # on_delete = models.CASCADE 级联删除，删除学生会连同档案一块删除
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'archives'
