import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

# 前后端分离，非DRF版
# 后端需要向前端提供JSON数据
from drf.models import Bookinfo


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
        },status=201)

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
