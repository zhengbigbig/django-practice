from datetime import datetime

from dateutil import tz

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader

from App02.forms import RegisterForm, LoginForm
# from myApp.models import User
from App02.models import User
from myApp.utils import send_email


def home(request):
    # 获取cookies 中指定键值对
    username = request.COOKIES.get('username')
    print(username)
    return render(request, 'App02/index.html', locals())


# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = User.objects.filter(username=username, password=password).first()
#         print(user.username)
#         if user:
#             response = redirect('/user/')
#             # 设置过期时间
#             future = datetime.now() + timedelta(days=3)
#             # 将cookie写回客户端
#             response.set_cookie('username', username, expires=future)
#             # 设置salt加密存储cookie数据
#             # response.set_signed_cookie()
#             return response
#     return render(request, 'App02/login.html')


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
            # 如果forms中表单的字段名和models模型的字段名一致可以如下写
            # res = User.objects.create(**data)
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


def register_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', "")
            password = request.POST.get('password', "")
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            # 验证用户是否存在
            user = User.objects.filter(username=username).first()
            if user:
                # 用户已存在
                return HttpResponse("用户已存在")
            else:
                # 保存用户
                User.objects.create_user(username=username,
                                         password=password,
                                         phone=phone,
                                         email=email)
                return HttpResponse("注册成功")
        except Exception as e:
            return HttpResponse('注册失败:' + e)
    else:
        return render(request, 'App02/register.html')


def index(request):
    # 在后端判断是否已经登录
    print(request.user.is_authenticated)
    print(request.user)
    return HttpResponse(f"是否登录 {request.user.is_authenticated}")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        # 用户验证，如果用户名和密码正确，返回User对象，否则返回None
        user = authenticate(request=request, username=username, password=password)
        print(user)
        if user:
            # 记录用户登录状态，参数是请求对象和用户对象
            # login() 将user写到session中并写到了request
            login(request=request, user=user)
            return HttpResponse('登录成功')
    return render(request, 'App02/login.html')


def user_logout(request):
    # 退出登录
    logout(request)
    return HttpResponse('已退出')


def update_password(request):
    username = request.user.username
    old_password = request.POST.get("oldPassword")
    new_password = request.POST.get("newPassword")
    user = auth.authenticate(username=username, password=old_password)
    if user:
        user.set_password(new_password)
        user.save()
        return HttpResponse("修改成功")
    else:
        return HttpResponse("修改失败")


def test_time(request):
    def utc_to_cst(date):
        from_zone = tz.gettz('UTC')
        print(from_zone)
        to_zome = tz.gettz('CST')
        utc_date = date.replace(tzinfo=from_zone)
        print(utc_date)
        cst_date = utc_date.astimezone(to_zome)
        print(cst_date)
        UTC_FORMAT = "%Y-%m-%d %H:%M:%S"
        time = datetime.strptime(str(cst_date)[:19], UTC_FORMAT)
        print(time)

    user = User.objects.filter(username='test').first()
    utc_to_cst(user.date_joined)
    return HttpResponse('xxx')


# 路由保护
@login_required(login_url='/user/login')
def publish(request):
    return HttpResponse("操作成功")


def captcha(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponse('验证通过')
        else:
            return render(request, 'App02/verifycode.html', locals())
    return render(request, 'App02/verifycode.html', locals())


# 邮箱
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives, EmailMessage
from django.conf import settings


# 发送一封邮件
def sendone(request):
    send_mail('title', 'content', settings.EMAIL_FROM, ['780357902@qq.com'])
    return HttpResponse('发送成功')


# 发送多封邮件
def sendmany(request):
    message1 = ('Subject here', '<b>test message</b>', settings.EMAIL_FROM, ['780357902@qq.com'])
    message2 = ('Subject here2', '<b>test message</b>', settings.EMAIL_FROM, ['780357902@qq.com'])
    send_mass_mail((message1, message2), fail_silently=False)
    return HttpResponse('发送成功')


# 渲染模板进行邮箱发送
def send_html_mail(request):
    subject, from_email, to = 'html', settings.EMAIL_FROM, '780357902@qq.com'
    html_content = loader.get_template('App02/active.html').render({'username': 'fk'})
    msg = EmailMultiAlternatives(subject, from_email=from_email, to=[to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return HttpResponse('html发送')


def custom_send(request):
    send_email(['780357902@qq.com'], '<b>test</b>')
    return HttpResponse('success')
