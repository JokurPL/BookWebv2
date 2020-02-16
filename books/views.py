from django.shortcuts import render
from django.http import HttpResponse 
from django.template import loader

from .models import Book

# Create your views here.
def index(request):
    books = Book.objects.order_by('-pub_date')[:5]
    context = {
        'books': books,
    }
    return render(request, 'books/index.html', context)

def book(request, book_id):
    return HttpResponse("Książka pt. %s" % book_id)

def author(request, book_id):
    return HttpResponse("Autor")

def category(request, book_id):
    return HttpResponse("Kategoria: ")