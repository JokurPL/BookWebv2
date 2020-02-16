from django.contrib import admin
from .models import Book, Author, Category
# Register your models here.
from django.db import models

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('book_likes',)
    fieldsets = [
        ('Ogólne informacje', {'fields':['book_title', 'book_author', 'book_desc', 'book_category', 'book_img', 'pub_date']}),
    ]

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
