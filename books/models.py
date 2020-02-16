from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    name = models.CharField("Autor", max_length=50)
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField("Kategoria", max_length=50)
    def __str__(self):
        return self.category_name


class Comment(models.Model):
    content = models.TextField("Treść komentarza", max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    pub_date = models.DateTimeField('Data utworzenia', auto_now_add=True)

    def __str__(self):
        return self.content[:10]


class Book(models.Model):
    book_title = models.CharField("Tytuł książki", max_length=50)
    book_desc = models.TextField("Opis książki", max_length=None)
    book_img = models.ImageField("Okładka książki", blank=True, null=True, upload_to="covers/%Y/%m/%D/")
    book_author = models.ManyToManyField(Author, verbose_name="Autor/Autorzy")
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria")
    pub_date = models.DateTimeField('Data utworzenia', auto_now_add=True)
    book_likes = models.IntegerField("Ocena", default=0)
    comments = models.ManyToManyField(Comment, verbose_name="Komentarze")

    def __str__(self):
        return self.book_title


