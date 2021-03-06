from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.db.models import Q
import matplotlib.pyplot as plt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
import json
from django.core.paginator import Paginator

from django.template import loader

from .models import *


def error_4xx(request, exception):
    return render(request, 'error.html')


def error_500(request):
    return render(request, 'error.html')


class IndexBooksView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.order_by('-pub_date')

        context = {
            'books': books,
        }
        return render(request, 'books/index.html', context)


class BookView(View):
    def get(self, request, book_id, *args, **kwargs):
        book = get_object_or_404(Book, pk=book_id)
        comments = Comment.objects.filter(book_id=book_id).order_by('-pub_date')
        paginator = Paginator(comments, 10)
        page_number = request.GET.get('strona')
        page_obj = paginator.get_page(page_number)
        title = book.book_title
        votes = book.rating_set.count()
        likes = Rating.objects.filter(book=book, like=True).count()
        if votes > 0:
            rate = (likes / votes) * 100
        else:
            rate = 0
        liked = False
        disliked = False
        if request.user.is_authenticated:
            user = request.user
            try:
                Rating.objects.get(user=user, book=book, like=True)
                liked = True
            except Rating.DoesNotExist:
                liked = False
            try:
                Rating.objects.get(user=user, book=book, dislike=True)
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
            'disliked': disliked,
            'page_obj': page_obj
        })


class AuthorsView(View):

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        context = {
            'authors': authors,
        }
        return render(request, 'authors/authors.html', context)


class AuthorView(View):
    def get(self, request, author_id, *args, **kwargs):
        author = get_object_or_404(Author, pk=author_id)

        context = {
            'author': author
        }
        return render(request, 'authors/author.html', context)


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
        update_book_rating(book)
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
            update_book_rating(book)
            return HttpResponse('')
        except Rating.DoesNotExist:
            try:
                rating = Rating.objects.get(
                    user=user,
                    book=book,
                    like=True
                )
                update_book_rating(book)
                return HttpResponse('')
            except Rating.DoesNotExist:
                Rating.objects.create(
                    user=user,
                    book=book,
                    like=True,
                    dislike=False
                )
                update_book_rating(book)
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
            update_book_rating(book)
            return HttpResponse('')
        except Rating.DoesNotExist:
            try:
                rating = Rating.objects.get(
                    user=user,
                    book=book,
                    dislike=True,
                    like=False
                )
                update_book_rating(book)
                return HttpResponse('')
            except Rating.DoesNotExist:
                Rating.objects.create(
                    user=user,
                    book=book,
                    like=False,
                    dislike=True
                )
                response_data = 'success'
                update_book_rating(book)
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


def category(request, category_id):
    return HttpResponse("Kategoria: %s" % category_id)


def update_book_rating(book):
    try:
        likes = Rating.objects.filter(like=True, book=book).count()
        print("lajki: %s " % likes)
    except Rating.DoesNotExist:
        likes = 0
    try:
        dislikes = Rating.objects.filter(dislike=True, book=book).count()
    except Rating.DoesNotExist:
        dislikes = 0
    rating = (likes / (likes + dislikes)) * 100
    book.book_rate = int(rating)
    book.save()
