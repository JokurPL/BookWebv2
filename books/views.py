from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader

from .models import *

# Create your views here.
def index(request):
    books = Book.objects.order_by('-pub_date')[:5]
    context = {
        'books': books,
    }
    return render(request, 'books/index.html', context)

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    comments = Comment.objects.filter(book_id=book_id)
    return render(request, 'books/book.html', {
        'book':book,
        'comments':comments,
    })

def author(request, book_id):
    return HttpResponse("Autor")

def category(request, book_id):
    return HttpResponse("Kategoria: ")