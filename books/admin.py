from django.contrib import admin
from .models import Book, Author, Category, Comment
# Register your models here.
from django.db import models

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('book_likes', 'pub_date')
    fieldsets = [
        ('Ogólne informacje', {'fields':['book_title', 'book_author', 'book_desc', 'book_category', 'book_img', 'pub_date']}),
        ('Informacje od użytkowników', {'fields': ['book_likes', 'comments', ]}),
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)