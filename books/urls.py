from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    #path('szukaj/<query>', views.search, name='search'),
    path('<book_id>/', views.book, name='book'),
    path('<book_id>/autor/', views.author, name='book_autor'),
    path('<book_id>/kategoria/', views.category, name='book_category'),
    path('<book_id>/dodaj-komentarz', views.book_add_comment, name='book_add_comment'),
    path('<book_id>/plus', views.vote_plus, name='book_plus'),
    path('<book_id>/minus', views.vote_minus, name='book_minus'),

]