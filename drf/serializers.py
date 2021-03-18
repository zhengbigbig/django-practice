import re

from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from drf.models import User, Bookinfo, Heroinfo


def validate_username_exist(value):
    if User.objects.filter(username=value).first():
        raise serializers.ValidationError('%s 用户名已存在' % value)


def validate_password(password):
    if re.math(r'\d+$', password):
        raise serializers.ValidationError("密码不能是纯数字")


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(required=True, validators=[
        validate_username_exist,
        RegexValidator(regex='^[a-zA-Z][a-zA-Z0-9_]{3,18}$', message='支持大小写字母数字下划线短横线')], error_messages={
        'required': '用户名必须输入', 'min_length': '用户名至少3个字符'
    })
    password_hash = serializers.CharField(required=True, validators=[validate_password,
                                                                     RegexValidator(
                                                                         regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\w\W]{8,16}$',
                                                                         message='必须包含大小写字母数字。可特殊符号',
                                                                     )])
    age = serializers.IntegerField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password_hash = validated_data.get('password_hash', instance.password_hash)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance


# class BookInfoSerializer(serializers.Serializer):
#     """图书数据序列化器"""
#     bid = serializers.IntegerField(label='ID', read_only=True, help_text="主键")
#     btitle = serializers.CharField(label='名称', max_length=20)
#     bpub_date = serializers.DateField(label='发布日期', required=False)
#     bread = serializers.IntegerField(label='阅读量', required=False)
#     bcomment = serializers.IntegerField(label='评论量', required=False)
#     bimage = serializers.CharField(label='图片', required=False)
#
#     def create(self, validated_data):
#         return Bookinfo.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.btitle = validated_data.get('btitle', instance.btitle)
#         instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
#         instance.bread = validated_data.get('bread', instance.bread)
#         instance.bcomment = validated_data.get('bcomment', instance.bcomment)
#         instance.save()
#         return instance

class HeroInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heroinfo
        fields = "__all__"


class BookInfoSerializer(serializers.ModelSerializer):
    heros = HeroInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Bookinfo
        fields = "__all__"
