from django.urls import path, re_path
from . import views

urlpatterns = [
    # 不能以/ 开头
    # 参数：路由匹配 视图函数 路由名称
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    # string
    path('change/<name>/', views.change_name, name='change'),
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

    # re_path(r'^user/$', views.handle_data, name='handle_data'),
    re_path(r'^filter/$', views.filter, name='filter'),
    re_path(r'^not_filter/$', views.not_filter, name='not_filter'),
    re_path(r'^count_statics/$', views.count_statics, name='count_statics'),
    re_path(r'^raw_sql/$', views.raw_sql, name='raw_sql'),
    re_path(r'^custom_sql/$', views.custom_sql, name='custom_sql'),
    re_path(r'^manage_user/$', views.manage_user, name='manage_user'),

    re_path(r'^addstudent/$', views.addstudent, name='addstudent'),
    re_path(r'^addarchives/$', views.addarchives, name='addarchives'),
    re_path(r'^deletestudent/$', views.deletestudent, name='deletestudent'),
    re_path(r'^findstudent/$', views.findstudent, name='findstudent'),
    re_path(r'^findarchives/$', views.findarchives, name='findarchives'),
    re_path(r'^lookup/$', views.lookup, name='lookup'),
    re_path(r'^books/$', views.books, name='books'),

    re_path(r'^testBuyerAndGoods/$', views.testBuyerAndGoods, name='testBuyerAndGoods'),
    re_path(r'^pagination/$', views.pagination, name='pagination'),
    re_path(r'^upload/$', views.upload),
    # re_path(r'^savefile/$', views.savefile),

    # re_path(r'^cache/$', views.cache),
    re_path(r'^cache_data/$', views.cache_data),

    re_path(r'^check_user/$', views.check_user, name='check_user'),
    path('active/<token>/', views.active_user, name='active'),

]
