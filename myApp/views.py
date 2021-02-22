from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from myApp.models import Grades, Students


def index(request):
    return HttpResponse("hello world")


def details(request, num):
    return HttpResponse("detail-%s" % num)


def grades(request):
    # 去模板取数据
    gradesList = Grades.objects.all()
    # 将数据传递给模板，模板再渲染页面，将渲染好的页面返回给浏览器
    return render(request, 'myApp/grades.html', {"grades": gradesList})


# 分页
def students(request, page):
    # 去模板取数据
    page = int(page)
    studentsList = Students.stuObj.all()[(page - 1) * 5:page * 5]
    # 将数据传递给模板，模板再渲染页面，将渲染好的页面返回给浏览器
    return render(request, 'myApp/students.html', {"students": studentsList})


def gradeStudents(request, num):
    grade = Grades.objects.get(pk=num)
    studentsList = grade.students_set.all()
    return render(request, 'myApp/students.html', {"students": studentsList})


def createStudent(request):
    grade = Grades.objects.get(pk=1)
    stu = Students.createStudent('x', 12, True, 'xxx', grade, '2021-02-22', False)
    stu.save()
    return HttpResponse("successful")


def createStudent2(request):
    grade = Grades.objects.get(pk=1)
    stu = Students.stuObj.createStudent('x', 12, True, 'xxx', grade, '2021-02-22', False)
    stu.save()
    return HttpResponse("successful2")
