from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from myApp.models import User


def validate_username_exist(value):
    if User.objects.filter(username=value).first():
        raise ValidationError('%s 用户名已存在' % value)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, validators=[
        validate_username_exist,
        RegexValidator(regex='^[a-zA-Z][a-zA-Z0-9_]{3,18}$', message='支持大小写字母数字下划线短横线')], error_messages={
        'required': '用户名必须输入', 'min_length': '用户名至少3个字符'
    })
    password = forms.CharField(required=True, validators=[
        RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\w\W]{8,16}$', message='必须包含大小写字母数字。可特殊符号',
                       )])
    rePassword = forms.CharField(required=True, validators=[
        RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\w\W]{8,16}$', message='必须包含大小写字母数字。可特殊符号',
                       )])
    createTime = forms.DateTimeField(required=False, error_messages={
        'invalid': '日期格式错误'
    })

    # 单个字段验证 clean_password
    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        return password

    def clean(self):
        password = self.cleaned_data.get('password', None)
        rePassword = self.cleaned_data.get('rePassword', '')
        if password != rePassword:
            raise ValidationError("两次密码输入不一致")
        return self.cleaned_data


class LoginForm(forms.Form):
    captcha = CaptchaField()  # 验证码字段
