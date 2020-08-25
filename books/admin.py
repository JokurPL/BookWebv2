from django.contrib import admin
from .models import Book, Author, Category, Comment, Rating
# Register your models here.
from django.db import models

admin.site.site_header = "BookWeb"


class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date', 'book_rate')
    fieldsets = [
        ('Ogólne informacje',
         {'fields': ['book_title', 'book_author', 'book_desc', 'book_category', 'book_img', 'book_rate', 'pub_date']}),
    ]


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('like', 'dislike', 'user', 'book')


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('content', 'user', 'book')

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
