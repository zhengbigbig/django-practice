from django.urls import path, re_path
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
]
