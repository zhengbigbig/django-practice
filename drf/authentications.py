import itsdangerous
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from drf.models import User
from myApp.email_token import token_confirm


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1. 获取token
        # token可以从请求的get参数中获取
        token = request.query_params.get('token')
        try:
            uid = token_confirm.confirm_validate_token(token, expiration=30)
        except itsdangerous.exc.SignatureExpired as e:  # token 过期
            raise AuthenticationFailed('token已过期')
        except:
            return None  # 认证不通过
        # 如果获取到uid
        # 查询数据库，获取用户信息
        try:
            user = User.objects.get(pk=uid)
        except:
            print('数据库访问错误')
            return None
        # 如果找到了用户，认证成功
        return (user, None) # 第二值,request auth可以获取
