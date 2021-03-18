from django.urls import path

from . import views

urlpatterns = [
    path('book/<int:bid>/', views.BookInfoView.as_view(), name='book'),
    path('book/', views.BookInfoView.as_view(), name='book'),

]
