from django.urls import path, re_path
from . import views

urlpatterns = [
    # 不能以/ 开头
    # 参数：路由匹配 视图函数 路由名称
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    # string
    path('change/<name>/',views.change_name,name='change'),
    # int
    path('show/<int:age>/', views.show, name='show'),
    # slug
    path('list/<slug:name>/', views.list_user, name='list'),
    # path，如果有多个参数，path类型必须在最后一个
    path('access/<path:path>/', views.access, name='access'),
    re_path(r'^tel/(1[3-9]\d{9})/$', views.get_phone, name='phone'),
    re_path(r'^tel/(?P<tel>1[3-9]\d{9})/$', views.get_tel, name='tel'),
    re_path(r'^request/$', views.request, name='request'),
    re_path(r'^good/$', views.good, name='good'),
    re_path(r'^handle2/$', views.handle2, name='handle2'),

    re_path(r'^red/$', views.handle_redirect, name='handle_redirect'),
    re_path(r'^blue/$', views.handle_redirect2, name='handle_redirect2'),
    re_path(r'^green/$', views.handle_redirect4, name='handle_redirect4'),

]
