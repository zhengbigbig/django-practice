from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
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
