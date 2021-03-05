from datetime import datetime, timedelta
import hashlib

from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from App02.forms import RegisterForm
from myApp.models import User


def home(request):
    # 获取cookies 中指定键值对
    username = request.COOKIES.get('username')
    print(username)
    return render(request, 'App02/index.html', locals())


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        print(user.username)
        if user:
            response = redirect('/user/')
            # 设置过期时间
            future = datetime.now() + timedelta(days=3)
            # 将cookie写回客户端
            response.set_cookie('username', username, expires=future)
            # 设置salt加密存储cookie数据
            # response.set_signed_cookie()
            return response
    return render(request, 'App02/login.html')


def logout(request):
    res = redirect('/user/')
    res.delete_cookie('username')
    return res


# 装饰器，路由保护
def check_login(func):
    def inner(*args, **kwargs):
        if args[0].COOKIES.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect('/user/login')

    return inner


@check_login
def list_article(request):
    return HttpResponse('articles')


from django.contrib.auth.hashers import make_password, check_password


# session操作
def doregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # md5 = hashlib.md5()
        # md5.update(password.encode())
        # password_md5 = md5.hexdigest()

        user = User(username=username,
                    password=make_password(password, None, 'pbkdf2_sha256'),
                    )
        try:
            user.save()
        except IntegrityError:
            return JsonResponse({
                'code': 0,
                'msg': '用户名重复',
            })
        except Exception as e:
            print(type(e))
        # 设置session
        request.session['username'] = username
        return JsonResponse({
            'code': 1,
            'msg': '注册成功',
        })
    return render(request, 'App02/register.html')


def validate_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if check_password(password, User.objects.get(username=username).password):
            return HttpResponse('success')
    return HttpResponse('fail')


def session(request):
    # session获取
    # username = request.session.get('username')
    # 清空session
    # request.session.clear() # 清除所有session键值对，不清空sessionid
    request.session.flush()  # 清除所有session键值对，并清空sessionid和数据库对应记录

    return JsonResponse('xxx', safe=False)


# Form
def register(request):
    if request.method == 'POST':
        # 用提交的数据生成表单
        form = RegisterForm(request.POST)
        ret = {'code': 0, 'msg': None}
        # 能通过验证，返回True，否则返回False
        if form.is_valid():
            # 进行业务处理
            data = form.cleaned_data
            print(data, 'create')
            data['password'] = make_password(form.cleaned_data['password'])
            User.objects.create(**data)
            ret['msg'] = 'ok'
            return JsonResponse(ret)
        else:
            # return render(request, 'App02/register.html',{'form':form})
            print(form.errors, type(form.errors))
            ret['msg'] = form.errors
            # ret['msg'] = list(form.errors.items())[0][1][0]
            return JsonResponse(ret)
    return render(request, 'App02/register.html')
