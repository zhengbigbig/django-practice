from django.contrib import admin

# Register your models here.
from .models import Grades, Students,Text


# 注册
class StudentsInfo(admin.TabularInline):
    model = Students
    extra = 2


@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    inlines = [StudentsInfo]
    # 列表列属性
    # 显示字段
    list_display = ['pk', 'gName', 'gDate', 'gGirlNum', 'gBoyNum', 'isDelete']
    # 过滤字段
    list_filter = ['gName', 'gDate']
    # 搜索字段
    search_fields = ['gName']
    # 分页
    list_per_page = 10

    # 添加、修改页属性，fields和fieldsets不能同时使用
    # 规定属性的先后顺序
    # fields = ['gName', 'gGirlNum', 'gBoyNum', 'isDelete', 'gDate']
    # 给属性分组
    fieldsets = [
        ("num", {"fields": ['gGirlNum', 'gBoyNum']}),
        ("base", {"fields": ['gName', 'gDate', 'isDelete']}),
    ]
    # 创建班级时添加student


# admin.site.register(Grades, GradesAdmin)


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    # 布尔值显示问题
    def gender(self):
        if self.sGender:
            return '男'
        else:
            return '女'

    # 设置页面列名称
    gender.short_description = '性别'
    list_display = ['pk', 'sName', 'sAge', gender, 'sContEnd', 'sGrade', 'isDelete']
    list_per_page = 10
    # 执行动作的位置
    actions_on_top = False
    actions_on_bottom = True


# admin.site.register(Students, StudentsAdmin)

admin.site.register(Text)
