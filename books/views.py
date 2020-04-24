from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View
import matplotlib.pyplot as plt

from django.template import loader

from .models import *


class IndexBooksView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.order_by('-pub_date')[:5]
        context = {
            'books': books,
        }
        return render(request, 'books/index.html', context)


def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    comments = Comment.objects.filter(book_id=book_id)
    user_count = book.book_likes + book.book_dislikes
    title = book.book_title
    name_session_plus = 'voted_plus_' + str(book_id)
    name_session_minus = 'voted_minus_' + str(book_id)
    is_minus = request.session.get(name_session_minus)
    is_plus = request.session.get(name_session_plus)
    if user_count > 0:
        rate = (book.book_likes / user_count) * 100
    else:
        rate = 0
    return render(request, 'books/book.html', {
        'book': book,
        'title': title,
        'comments': comments,
        'rate': round(rate),
        'request': request,
        'is_plus': is_plus,
        'is_minus': is_minus,
    })


def book_add_comment(request, book_id):
    nick = request.POST['nick']
    content = request.POST['content']
    book = get_object_or_404(Book, pk=book_id)
    comment = Comment(user=nick, content=content, book=book)
    comment.save()
    return HttpResponseRedirect(reverse('books:book', args=(book_id,)))


def vote_plus(request, book_id):
    name_session_plus = 'voted_plus_' + str(book_id)
    name_session_minus = 'voted_minus_' + str(book_id)
    book = get_object_or_404(Book, pk=book_id)
    if request.session.get(name_session_plus, True):
        if book.book_dislikes > 0:
            book.book_dislikes -= 1
        book.book_likes += 1
        book.save()
        request.session[name_session_plus] = False
        request.session[name_session_minus] = True
        request.session.save()
    return HttpResponseRedirect(reverse('books:book', args=(book_id,)))


def vote_minus(request, book_id):
    name_session_plus = 'voted_plus_' + str(book_id)
    name_session_minus = 'voted_minus_' + str(book_id)
    if request.session.get(name_session_minus, True):
        book = get_object_or_404(Book, pk=book_id)
        if book.book_likes > 0:
            book.book_likes -= 1
        book.book_dislikes += 1
        book.save()
        request.session[name_session_plus] = True
        request.session[name_session_minus] = False
        request.session.save()
    return HttpResponseRedirect(reverse('books:book', args=(book_id,)))


def author(request, book_id):
    return HttpResponse("Autor")


def category(request, book_id):
    return HttpResponse("Kategoria: ")
