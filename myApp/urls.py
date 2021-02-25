from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(\d+)$', views.details),
    re_path(r'^grades/$', views.grades),
    re_path(r'^students/(\d+)/$', views.students),
    re_path(r'^grades/(\d+)/$', views.gradeStudents),
    re_path(r'^addstudent/$', views.createStudent),
    re_path(r'^addstudent2/$', views.createStudent2),
    re_path(r'^attribles', views.attribles),
    re_path(r'^post1/', views.post1),
    re_path(r'^showResponse/', views.showResponse),
    re_path(r'^cookie/', views.cookie),
    re_path(r'^redirect1/', views.redirect1),
    re_path(r'^redirect2/', views.redirect2),

    re_path(r'^main/$', views.main, name='main'),
    re_path(r'^login/$', views.login),
    re_path(r'^user/login/$', views.userLogin),
    re_path(r'^logout$', views.quit),

    re_path(r'^verifycode/$', views.verifycode),
    re_path(r'^verifycodehtml/$', views.verifycodehtml),
    re_path(r'^verifycodecheck/$', views.verifycodecheck),
    re_path(r'^upload/$', views.upload),
    re_path(r'^savefile/$', views.savefile),

    re_path(r'^studentpage/$',views.studentpage)
]
