import json
import sys

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response

from project.settings import BLACKLIST


class MyMiddle(MiddlewareMixin):
    def process_request(self, request):
        print(request.META['REMOTE_ADDR'])
        # 网站统计
        # if request.is_ajax():
        #     statics = CountStatics.objects.get(path=request.path)
        #     statics.count += 1
        #     statics.save()
        # 黑名单
        if request.META['REMOTE_ADDR'] in BLACKLIST:
            return HttpResponse('本站拒绝访问')
        # 登录判断
        path = request.path
        print(request.user, path)
        if not request.user.is_authenticated and path != '/user/user_login/':
            return redirect(reverse("App02:user_login"))

    # 统一返回json数据
    def process_response(self, request, response):
        # 类型判断
        if isinstance(response, (dict, list)):
            result = json.dumps(response)
            # 必须返回数据
            return HttpResponse(result)
        return response

    def process_exception(self, request, exception):
        # 对管理员展示错误界面，一般用户只能看到404，500等页面
        ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1':
            return technical_500_response(request, *sys.exc_info())
        return redirect(reverse("App02:index"))
