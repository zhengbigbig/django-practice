from django.utils.deprecation import MiddlewareMixin


class MyMiddle(MiddlewareMixin):
    def process_request(self, request):
        print('hahaha')
