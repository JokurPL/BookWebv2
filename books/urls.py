from django.urls import path

from . import views
from books.views import IndexBooksView, BookView, AuthorsView

app_name = 'books'
urlpatterns = [
    path('ksiazki/', IndexBooksView.as_view(), name='index'),
    path('autorzy/', AuthorsView.as_view(), name='authors'),
    path('szukaj/', views.search, name='search'),
    path('<book_id>/', BookView.as_view(), name='book'),
    path('autor/<author_id>', views.author, name='book_author'),
    path('<book_id>/kategoria/', views.category, name='book_category'),
    path('<book_id>/dodaj-komentarz', views.book_add_comment, name='book_add_comment'),
    path('<book_id>/plus', views.vote_plus, name='book_plus'),
    path('<book_id>/minus', views.vote_minus, name='book_minus'),
]