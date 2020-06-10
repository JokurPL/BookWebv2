from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.db.models import Q
import matplotlib.pyplot as plt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
import json
from django.template import loader

from .models import *


def error_4xx(request, exception):
    return render(request, 'error.html')


def error_500(request):
    return render(request, 'error.html')


class IndexBooksView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.order_by('-pub_date')[:5]
        context = {
            'books': books,
        }
        return render(request, 'books/index.html', context)


class BookView(View):
    def get(self, request, book_id, *args, **kwargs):
        book = get_object_or_404(Book, pk=book_id)
        comments = Comment.objects.filter(book_id=book_id).order_by('-pub_date')
        title = book.book_title
        votes = book.rating_set.count()
        likes = Rating.objects.filter(book=book, like=True).count()
        if votes > 0:
            rate = (likes / votes) * 100
        else:
            rate = 0
        liked = False
        disliked = False
        if request.user:
            try:
                Rating.objects.get(user=request.user, book=book, like=True)
                liked = True
            except Rating.DoesNotExist:
                liked = False
            try:
                y = Rating.objects.get(user=request.user, book=book, dislike=True)
                disliked = True
            except Rating.DoesNotExist:
                disliked = False
        return render(request, 'books/book.html', {
            'book': book,
            'title': title,
            'comments': comments,
            'request': request,
            'votes': votes,
            'rate': round(rate),
            'liked': liked,
            'disliked': disliked
        })


class AuthorsView(View):

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        context = {
            'authors': authors,
        }
        return render(request, 'authors/authors.html', context)


def author(request, author_id):
    return HttpResponse(author_id)


def log_in(request):
    if request.is_ajax() and request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        response_data = {}
        if user is not None:
            login(request, user)
            response_data['result'] = 'success'
        else:
            response_data['result'] = 'failed'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def register_user(request):
    if request.is_ajax() and request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        email = request.POST['email']
        response_data = {}
        if password != password_repeat:
            response_data['result'] = 'failed'
        else:
            group = Group.objects.get(name='user')
            try:
                user = User.objects.get(username=username)
                response_data['result'] = 'username_exist'
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=email)
                    response_data['result'] = 'email_exist'
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                    )
                    user.groups.add(group)
                    user.save()
                    login(request, user)
                    response_data['result'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def log_out(request):
    logout(request)
    return HttpResponse('')


def book_add_comment(request, book_id):
    if request.is_ajax() and request.method == 'POST':
        user = get_object_or_404(User, pk=request.POST['user_id'])
        content = request.POST['content']
        book = get_object_or_404(Book, pk=book_id)
        comment = Comment(user=user, content=content, book=book)
        comment.save()
        return HttpResponse('')


def vote_plus(request, book_id):
    if request.is_ajax() and request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        user = request.user
        response_data = {}
        try:
            rating = Rating.objects.get(
                user=user,
                book=book,
                dislike=True,
                like=False
            )
            rating.like = True
            rating.dislike = False
            rating.save()
            return HttpResponse('')
        except Rating.DoesNotExist:
            try:
                rating = Rating.objects.get(
                    user=user,
                    book=book,
                    like=True
                )
                return HttpResponse('')
            except Rating.DoesNotExist:
                Rating.objects.create(
                    user=user,
                    book=book,
                    like=True,
                    dislike=False
                )
                return HttpResponse('')


def vote_minus(request, book_id):
    if request.is_ajax() and request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        user = request.user
        response_data = {}
        try:
            rating = Rating.objects.get(
                user=user,
                book=book,
                like=True,
                dislike=False
            )
            rating.like = False
            rating.dislike = True
            rating.save()
            return HttpResponse('')
        except Rating.DoesNotExist:
            try:
                rating = Rating.objects.get(
                    user=user,
                    book=book,
                    dislike=True,
                    like=False
                )
                return HttpResponse('')
            except Rating.DoesNotExist:
                Rating.objects.create(
                    user=user,
                    book=book,
                    like=False,
                    dislike=True
                )
                response_data = 'success'
                return HttpResponse('')


def search(request):
    query = request.POST['query']
    try:
        books = Book.objects.filter(Q(book_title__icontains=query) | Q(book_author__name__icontains=query) | Q(
            book_category__category_name__icontains=query))
    except Book.DoesNotExist:
        books = None
    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'books/search_query.html', context)


def category(request, book_id):
    return HttpResponse("Kategoria: ")
