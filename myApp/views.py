import os
from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse


def home(request):
    return HttpResponse('hello world')


def show(request, age):
    print(type(age))
    return HttpResponse(str(age))


def list_user(request, name):
    print(type(name))
    return HttpResponse(name)


def access(request, path):
    return HttpResponse(path)


def get_phone(request, tel):
    return HttpResponse(str(tel))


def get_tel(request, tel):
    return HttpResponse(str(tel))


def change_name(request, name):
    return HttpResponse(name)


def request(request):
    # get传参获取
    print(request.GET)
    # 获取单一值
    print(request.GET.get('username'))
    # 获取一个返回值列表
    print(request.GET.getlist('age'))

    # post
    print(request.POST.get('username'))
    print(request.POST.getlist('age'))
    print(request.body.decode())

    # 获取请求方法
    print(request.method)
    # 获取请求路径
    print(request.path)
    print(request.get_full_path())
    print(request.get_host())
    print(request.get_raw_uri())
    print(request.build_absolute_uri())
    print(request.get_full_path_info())
    # 判断是否是ajax
    print(request.is_ajax())
    # 其他属性
    # print(request.META)
    # 客户端地址
    print(request.META.get('REMOTE_ADDR'))
    # 来源页面
    print(request.META.get('HTTP_REFERER'))
    # 获取请求参数的字典
    print(request.GET.dict())

    return HttpResponse('test')


def good(req):
    # res = HttpResponse()
    # res.content = b'good'
    # res.charset = 'utf-8'
    # res.content_type = 'text/html'
    # res.status_code = 200
    # return res
    return HttpResponse(b'good', status=400, charset='utf-8', content_type='text/html')


def handle(req, data):
    return render(request, 'myApp/index.html', {'data': data})


import json


def handle2(req):
    # 直接返回字典
    # return JsonResponse({'name': 'xxx'})
    # return JsonResponse(json.dumps({'name': 'xxx'})) 等同于上面
    # 返回非字典
    return JsonResponse([1, 2, 3, 4, 5], safe=False)


# 重定向
def handle_redirect(request):
    # return HttpResponseRedirect('/main')
    return redirect('/main')


# 带参数重定向
def handle_redirect2(req):
    return redirect("/home/{}/{}/".format('xxx', 30))


# 应用内跳转和应用外跳转
def handle_redirect3(req):
    # 应用内跳转可以不写http://127.0.0.1:8000
    # return redirect("/home")
    # 应用外跳转
    return redirect("https://www.baidu.com")


# 反向定位：由应用命名空间:name来确定路由
# 正向：路由->视图函数 反向：由名称来确定路由
def handle_redirect4(req):
    # return redirect(reverse("myApp:home"))  # 不带参数
    return redirect(reverse('myApp:list', kwargs={'name': 'admin'}))
    # return redirect(reverse('myApp:list', args=('xxx')))


from django.template import loader


def index(request):
    temp = loader.get_template('myApp/index.html')
    # 渲染模板，生成Html源码
    print(datetime.now())
    res = temp.render(context={'time': datetime.now()})
    # print(res)
    return HttpResponse(res)
