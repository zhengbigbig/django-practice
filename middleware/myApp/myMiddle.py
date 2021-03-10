from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from project.settings import BLACKLIST


class MyMiddle(MiddlewareMixin):
    def process_request(self, request):
        print(request.META['REMOTE_ADDR'])
        # 网站统计
        # 黑名单
        if request.META['REMOTE_ADDR'] in BLACKLIST:
            return HttpResponse('本站拒绝访问')

        # 登录判断
        username = request.session.get('username')
        path = request.path
        print(username,path)
        if not username and path != '/users/login/':
            return redirect(reversed("myApp:login"))

    # 统一返回json数据
        
