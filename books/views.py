from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

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
    user_count = book.book_likes + book.book_dislikes
    if user_count > 0:
        rate = (book.book_likes / user_count)*100
    else:
        rate = 0
    return render(request, 'books/book.html', {
        'book': book,
        'comments': comments,
        'rate': round(rate),
    })


# def vote_plus(request, book_id):
#     if request.session.get('voted_plus', False):
#         book = get_object_or_404(Book, pk=book_id)
#         book.book_dislikes -= 1
#         book.book_likes += 1
#         book.save()
#         request.session['voted_plus'] = False
#         request.session['voted_minus'] = False
#     return HttpResponseRedirect(reverse('books:book', args=(book_id,)))


# def vote_minus(request, book_id):
#     if request.session.get('voted_minus', False):
#         book = get_object_or_404(Book, pk=book_id)
#         book.book_likes -= 1
#         book.book_dislikes += 1
#         book.save()
#         request.session['voted_minus'] = True
#         request.session['voted_plus'] = False
#     return HttpResponseRedirect(reverse('books:book', args=(book_id,)))


def author(request, book_id):
    return HttpResponse("Autor")


def category(request, book_id):
    return HttpResponse("Kategoria: ")
