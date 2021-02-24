from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from myApp.models import Grades, Students
import json


def attribles(request):
    print(request.path)
    print(request.method)
    print(request.encoding)
    print(request.GET)
    print(request.POST)
    print(request.FILES)
    print(request.COOKIES)
    print(request.session)
    return HttpResponse('attr')


# 访问/get1?a=1&b=2&c=3


def get1(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    c = request.GET['c']
    return HttpResponse(a + ' ' + b + ' ' + c)


# 访问/get1?a=1&b=2&c=3&a=4
def get2(request):
    a = request.GET.getlist('a')
    b = request.GET.get('b')
    c = request.GET['c']
    return HttpResponse(a[0] + '' + a[1] + ' ' + b + ' ' + c)


def showResponse(request):
    res = HttpResponse()
    print(res.content)
    res.content = b'good'
    print(res.charset)
    print(res.status_code)
    print(res['content-type'])
    return res


def cookie(request):
    res = HttpResponse()
    c = request.COOKIES
    print(c)
    cookie = res.set_cookie("x", "y")
    return res


# 表单提交和body传参
def post1(request):
    # 表单提交提取
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username, password)
    # body提交提取
    print(json.loads(request.body))

    return HttpResponse('x')


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


# 重定向
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def redirect1(request):
    # return HttpResponseRedirect('/redirect2')
    return redirect('/redirect2')


def redirect2(request):
    return HttpResponse("重定向后")


def main(request):
    # 取session
    username = request.session.get('username', '游客')
    print(username)
    return render(request, 'myApp/main.html', {'username': username})


def login(request):
    return render(request, 'myApp/login.html')


def userLogin(request):
    print('xxxx')
    username = request.POST.get('username')
    # 存储session
    request.session['username'] = username
    print(username)
    return redirect('/main')


from django.contrib.auth import logout


def quit(request):
    # 清楚session
    # logout(request)
    # request.session.clear()
    request.session.flush()
    return redirect('/main')


def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)

    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值

    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    font = ImageFont.truetype(r'/Users/zhengzhiheng/Library/Fonts/华文行楷.ttf', 40)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字

    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def verifycodehtml(request):
    f = request.session.get('flag', True)
    str = ''
    if f == False:
        str = '请重新输入'
    request.session.clear()
    return render(request, 'myApp/verifycode.html', {"flag": str})


def verifycodecheck(request):
    code1 = str(request.POST.get("verifycode")).upper()
    code2 = str(request.session['verifycode']).upper()
    print(code1, code2)
    if code1 == code2:
        return redirect('/main')
    else:
        request.session['flag'] = False
        return redirect('/verifycodehtml')
