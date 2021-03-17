from django.urls import path

from . import views

urlpatterns = [
    path('book/<int:bid>/', views.BooksView.as_view(), name='book'),
]
