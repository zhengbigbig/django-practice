from django.contrib import admin

# Register your models here.
from .models import User


@admin.register(User)
class GradesAdmin(admin.ModelAdmin):
    # 列表列属性
    # 显示字段
    list_display = ['id', 'username', 'password', 'createTime']
    # 过滤字段
    list_filter = ['username']
    # 搜索字段
    search_fields = ['username']
    # 分页
    list_per_page = 10
