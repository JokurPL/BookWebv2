from django.urls import path

from . import views

app_name='books'
urlpatterns = [
    path('', views.index, name='index'),
    path('<book_id>/', views.book, name='book'),
    path('<book_id>/autor/', views.author, name='book_autor'),
    path('<book_id>/kategoria/', views.category, name='book_category'),
]