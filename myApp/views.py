import json
import random
from datetime import datetime

from django.core import serializers
# Create your views here.
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from App02.models import User
from myApp.email_token import token_confirm
from myApp.models import Publisher, Book, Goods, Buyer
from myApp.models1 import Student, Archives
from myApp.utils import CustomPaginator, FileUpload
from project.settings import EMAIL_FROM


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


# 局部禁用csrf
@csrf_exempt
def handleAjax(request):
    if request.is_ajax():
        return JsonResponse({"code": 0, "msg": 'success'})
    return render(request, 'myApp/ajax.html')


def handle_data(request):
    # 增加
    # user = User(username='tom', password=md5(b'123').hexdigest())
    # user.save()
    # 便捷插入
    # User.objects.create(username='tom1', password=md5(b'123').hexdigest())

    # user = {'username':'xx','password':'asdasd'}
    # User.objects.create(**user)
    # 批量插入
    User.objects.bulk_create([User(username='u111', password='p1'), User(username='u222', password='p1')])
    # 修改
    # user = User.objects.get(pk=1)
    # user.password = '233'
    # user.save()

    # 删除
    # try:
    #     user = User.objects.get(id=1)
    #     print(user, type(user))
    #     if user:
    #         user.delete()
    # except Exception as e:
    #     print(e)
    # 删除多条
    # users = User.objects.filter(id__gte=2)
    # print(users)
    # users.delete()

    return HttpResponse('xxx')


def filter(request):
    # 查询结果集 QuerySet
    # 1. all
    # select * from user
    allData = User.objects.all()
    # print(allData)
    # 2. first
    # data = data.first()
    # 3. filter
    # select * from user where id >= 5
    # data = data.filter(id__gte=5)
    # 4. exclude
    # data = allData.exclude(id__gte=25)
    # data2 = allData.filter(id__lt=25) # 等价
    # print(data,'-----',data2)
    # 5. order_by
    # data = allData.order_by('username')
    # print(data)
    # 6. 限制结果集 不支持负下标 从0 到 1
    # data = allData.order_by('id')[:2] # <QuerySet [<User: User object (21)>, <User: User object (22)>]>
    # 7. values
    # 返回所有字段
    # data = allData.values()
    # print(data)
    # 返回指定字段
    data = allData[0:1].values('username', 'password')
    print(data)  # <QuerySet [{'username': 'u1', 'password': 'p1'}]>
    for user in data:
        print(type(user), user)  # <class 'dict'> {'username': 'u1', 'password': 'p1'}
    # 8. reverse() 反序
    # data = allData.order_by('id')[:2].reverse()
    # 9. distinct 去重
    data2 = allData.values('password').distinct().order_by('password')[:10]
    return HttpResponse('xxx')


def not_filter(request):
    # 非过滤器方法
    # 1. get 只能返回一条记录，若记录不存在：DoesNotExist，若有多条：MultipleObjectsReturned
    # user = User.objects.get(id__gt=1)
    # 2. first last 返回一个模型对象，第一条和最后一条
    first_user = User.objects.first()
    last_user = User.objects.last()
    print(first_user, last_user)
    # 3. earliest 根据指定字段返回最早增加的记录
    # 4. latest 根据field字段返回最近增加记录
    # 5. exists 判断查询集是否有数据
    flag = User.objects.all().exists()
    print(flag)
    # 6. count 返回查询集中对象的数目
    count = User.objects.count()
    print(count)
    return HttpResponse('query')


from django.db.models import Max, Min, Count, Q, F


def count_statics(request):
    # 聚合查询：对多行查询结果的一列进行操作
    # select count(*) from user
    User.objects.aggregate(Count('id'))
    User.objects.aggregate(Max('id'))
    User.objects.aggregate(Min('id'))
    # 分组统计
    # select type,count(*) from user group by password
    res = User.objects.values('password').annotate(Count('id')).order_by('password')
    print(res)
    # 查看生成的sql语句
    print(res.query)

    # Q对象：构造逻辑或、逻辑非
    data = User.objects.filter(Q(id__gt=30) | Q(username__icontains='张'))
    data = User.objects.filter(~Q(sex=1))  # 不能处理null

    # F对象：
    data = User.objects.filter(username=F('password'))
    return HttpResponse('x')


# 原生sql语句使用
def raw_sql(request):
    # 多表联合查询
    # data = User.objects.raw("select * from user,detail where user.id = detail.user_id")
    # print(list(data))

    # 防止sql注入
    tmp = input('用户名:')
    users = User.objects.raw("select * from users where username like %s", ['%' + tmp + '%'])
    print(list(users), users)
    print(users.query)
    return HttpResponse(serializers.serialize('json', list(users)))


from django.db import connection


def custom_sql(request):
    # with语句相当于cursor = connection.cursor() 和cursor.close()
    # with connection.cursor() as cursor:
    #     cursor.execute("select * from users")
    #     row = cursor.fetchone()
    #     print(row)
    # 返回列表套字典
    with connection.cursor() as cursor:
        cursor.execute("select * from users")
        columns = [col[0] for col in cursor.description]
        print(cursor.fetchall())
        res = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(res)
    return HttpResponse('x')


def manage_user(request):
    data = User.userManager.all()
    print(data)
    return HttpResponse('x')


# 一对一
# 增加数据
def addstudent(request):
    Student.objects.create(sno="163212", sname='xxx', sage=14)
    return HttpResponse('add student successful')


def addarchives(request):
    stu = Student.objects.get(pk='163212')
    arc = Archives.objects.create(idcard='111111111111111111', student=stu)
    return HttpResponse('增加档案')


# 删除数据

def deletestudent(request):
    stu = Student.objects.get(pk='163212')
    stu.delete()
    return HttpResponse('删除成功')


# 正向查询 通过学生获取学生档案
def findstudent(request):
    stu = Student.objects.first()
    arc = stu.archives
    print(arc)
    return HttpResponse(arc)


# 反向查询 通过档案获取学生
def findarchives(request):
    arc = Archives.objects.first()
    stu = arc.student
    print(stu)
    return HttpResponse(stu)


# 跨关系查询
def lookup(request):
    # 根据档案查学生
    # student = Student.objects.get(archives__pk=2)
    student = Student.objects.get(archives__idcard='111111111111111111')
    print(student)
    # 根据学生查档案
    archives = Archives.objects.get(student__sno='163212')
    return HttpResponse(archives)


#
def books(request):
    # 创建一个出版社
    # pub = Publisher(pname='清华出版社')
    # pub.save()

    # 创建出版社并创建图书
    # pub = Publisher.objects.get(pk=2)
    # pub.books.create(bname='韭菜的个人修养')
    # books = Book.objects.filter(pk__lt=5)
    # pub.books.bulk_create(list(books))

    # 创建book
    # book = Book(bname='草根谭')
    # book.save()

    # 创建book并关联
    # pub = Publisher.objects.get(pk=1)
    # 方式1
    # book = Book.objects.create(bname='离骚2', publisher=pub)
    # 方式2
    # book = Book.objects.get(pk=2)
    # book.publisher = pub

    # 删除和更新
    # pub = Publisher.objects.get(pk=1)
    # pub.books.all().delete()  # 删除出版社出版的所有图书
    # pub.books.all().update(bname='xxx')

    # 查询 使用外键增删改查效率较低
    pub = Publisher.objects.get(pk=2)
    # pub.books 是一个查询管理器对象 objects
    print(pub.books.all())

    # 由图书查出版社
    book = Book.objects.get(pk=5)
    print(book.publisher.pname)

    # 复杂查询
    pub = Publisher.objects.filter(books__bname='韭菜的个人修养')
    print(pub)
    book = Book.objects.filter(publisher__isnull=True)
    print(book)
    return HttpResponse('success')


def testBuyerAndGoods(request):
    # good = Goods(gname='商品1',price=12.00)
    # good.save()
    # buyer = Buyer(bname='zzz', level=1)
    # buyer.save()
    # 购买商品
    goods = Goods.objects.get(pk=random.randint(1, Goods.objects.count()))
    goods.buyer.add(Buyer.objects.get(pk=random.randint(1, Buyer.objects.count())))
    goods.save()
    # 生成订单
    # order = Orders(buyer=Buyer.objects.get(pk=random.randint(1, Buyer.objects.count())),
    #                goods=Goods.objects.get(pk=random.randint(1, Goods.objects.count())),
    #                num=3)
    # order.save()
    # 删除商品
    # buyer = Buyer.objects.get(pk=1)
    # buyer.goods_set.clear()  # 删除所有商品
    # buyer.goods_set.remove(Goods.objects.get(pk=2)) # 删除用户Id=4订单中指定商品
    # orders = Orders.objects.filter(buyer__pk=1, goods__id__lt=5)
    # print(orders)
    # orders.delete()
    # 正向查询
    # buyer = Buyer.objects.get(pk=13)
    # goods = buyer.goods_set.all()
    # 反向查询
    good = Goods.objects.get(pk=3)
    buyers = good.buyer.all()
    print(buyers)
    return HttpResponse('success')


def pagination(request):
    page = request.GET.get('current', 1)
    pageSize = request.GET.get('pageSize', 10)
    allList = Goods.objects.all()
    # paginator = Paginator(allList, pageSize)
    # currentPageList = paginator.page(page)
    # print(list(currentPageList.object_list))
    currentPageList = CustomPaginator(allList, pageSize).lst(page)
    print(currentPageList)
    return HttpResponse('success')


from django.conf import settings


# def upload(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         print(file.name, file.size)
#         upload_path = os.path.join(settings.STATICFILES_DIRS[0],'upload')
#         if not os.path.exists(upload_path):
#             os.makedirs(upload_path)
#         save_path = os.path.join(upload_path, file.name)
#         print(save_path)
#         with open(save_path, 'wb') as f:
#             if file.multiple_chunks():
#                 for myf in file.chunks():
#                     f.write(myf)
#                 print('> 2.5M')
#             else:
#                 print('< 2.5')
#                 f.write(file.read())
#         return HttpResponse('文件上传')
#
#     else:
#         return render(request, 'myApp/upload.html')


def upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        path = settings.MEDIA_ROOT
        fp = FileUpload(file)
        tag = fp.upload(path)
        if tag > 0:
            return HttpResponse('上传成功')
        return HttpResponse('上传失败，请检查文件格式和大小')
    else:
        return render(request, 'myApp/upload.html')


from django.views.decorators.cache import cache_page

# @cache_page(5)
# def cache(request):
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#     print(current_time)
#     return render(request, 'myApp/cache.html', locals())
from django.core.serializers import serialize


def cache_data(request):
    # 首先判断数据是否在缓存中，如果在直接获取
    users = cache.get('all_users')
    print(users, '缓存')
    # 如果不在缓存，查询数据库，将结果写入缓存
    if not users:
        users = User.objects.all()
        cache.set('all_users', users)
    return HttpResponse(serialize('json', users))


# 邮箱验证

def check_user(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', "")
            password = request.POST.get('password', "")
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            # 验证用户是否存在
            user = User.objects.filter(username=username).first()
            if user:
                if not user.is_active:
                    return HttpResponse('请先激活')
                # 用户已存在
                return HttpResponse("用户已存在")
            else:
                # 保存用户
                User.objects.create_user(username=username,
                                                password=password,
                                                phone=phone,
                                                email=email,is_active = 0)
                # 发送邮件验证
                token = token_confirm.generate_validate_token(username)
                link = reverse("myApp:active", kwargs={'token': token})
                link = 'http://' + request.get_host() + link
                print(link)
                html = loader.get_template('myApp/active.html').render({'link': link})
                send_mail('账户激活', '', EMAIL_FROM, [email], html_message=html)
                return HttpResponse("请登录到注册邮箱中验证用户，有效期1小时")
        except Exception as e:
            return HttpResponse('注册失败:' + e)

    return render(request, 'myApp/register.html')


def active_user(request,token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username = username)
        users.delete()
        return HttpResponse('验证链接已经过期，请重新注册')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('验证用户不存在，请先注册')
    user.is_active = True
    user.save()
    return  HttpResponse('验证通过，请先登录')