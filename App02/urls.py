from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),

    # 路由保护
    path('list/', views.list_article, name='list'),
    path('doregister/', views.doregister, name='doregister'),
    path('session/', views.session, name='session'),
    path('register/', views.register, name='register'),
    path('register_view/', views.register_view, name='register_view'),
    path('user_login/', views.user_login, name='user_login'),
    path('test_time/', views.test_time, name='test_time'),
    path('index/', views.index, name='index'),
    path('publish/', views.publish, name='publish'),

    # 图形验证码
    path('captcha/', views.captcha, name='captcha'),
    # 邮箱发送
    path('sendone/', views.sendone, name='sendone'),
    path('sendmany/', views.sendmany, name='sendmany'),
    path('send_html_mail/', views.send_html_mail, name='send_html_mail'),
    path('custom_send/', views.custom_send, name='custom_send'),
]
