from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^(\d+)$', views.details),
    re_path(r'^grades/$', views.grades),
    re_path(r'^students/(\d+)/$', views.students),
    re_path(r'^grades/(\d+)/$', views.gradeStudents),
    re_path(r'^addstudent/$', views.createStudent),
    re_path(r'^addstudent2/$', views.createStudent2),
]
