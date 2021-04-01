import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

# 前后端分离，非DRF版
# 后端需要向前端提供JSON数据
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from drf.models import Bookinfo, User
from drf.serializers import UserSerializer, BookInfoSerializer


class BooksView(View):

    def queryset_to_list(self, queryset):
        res = []
        for obj in queryset:
            res.append(obj.to_dict())
        return res
    def get(self, request, *args, **kwargs):
        books = Bookinfo.objects.all()
        return JsonResponse(self.queryset_to_list(books), safe=False)

    def post(self, request):
        data = request.POST.dict()
        Bookinfo.objects.create(**data)
        return JsonResponse({
            'code': 1, 'msg': '创建成功'
        }, status=201)

    def put(self, request, bid):
        try:
            book = Bookinfo.objects.get(pk=bid)
        except Bookinfo.DoesNotExist:
            return HttpResponse(status=404)
        book_dict = json.loads(request.body.decode())
        book.__dict__.update(book_dict)
        book.save()
        return JsonResponse({
            'code': 1, 'msg': '修改成功'
        })

    def delete(self, request):
        pass


class ExampleView(APIView):
    def get(self, request):
        # 1. 查询数据
        user = User.objects.get(pk=1)
        # 2. 构造序列化器
        serializer = UserSerializer(instance=user)
        # 获取序列化数据，通过data属性可以获取序列化后的数据
        print(serializer.data)
        return Response(serializer.data)


class BookInfoView(GenericAPIView):
    """
    get:
    获取所有图书

    post:
    创建图书
    """
    queryset = Bookinfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request, bid=-1):
        if bid < 0:
            return self.find_many(request=request)
        return self.find_one(request, bid)

    def find_many(self, request):
        bs = BookInfoSerializer(instance=self.queryset.all(), many=True)
        return Response(data=bs.data)

    def find_one(self, request, bid):
        book = self.queryset.filter(pk=bid).first()
        bs = BookInfoSerializer(instance=book)
        return Response(data=bs.data)

    def post(self, request):
        # print(request.data)
        # 反序列化
        # 将前端传过来的数据赋值给data
        bs = BookInfoSerializer(data=request.data)
        if bs.is_valid():  # 数据验证
            print(bs.validated_data)  # 获取验证数据
            bs.save()  # 保存数据库
            return Response({'code': 1, 'msg': 'success'})
        else:
            print(bs.errors)
            return Response({'code': 0, 'msg': bs.errors})

    def put(self, request, bid):
        book = Bookinfo.objects.get(id=bid)
        # 部分更新
        # data = request.data
        # for key, value in data.items():
        #     if hasattr(book, key):
        #         setattr(book, key, value)
        # book.save()
        # 序列化器是必须满足序列化要求的
        bs = BookInfoSerializer(book, data=request.data)
        if bs.is_valid():  # 数据验证
            print(bs.validated_data)  # 获取验证数据
            bs.save()  # 保存数据库
            return Response({'code': 1, 'msg': 'success'})
        else:
            print(bs.errors)
            return Response({'code': 0, 'msg': bs.errors})
