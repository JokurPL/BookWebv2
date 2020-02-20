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

class Book(models.Model):
    book_title = models.CharField("Tytuł książki", max_length=50)
    book_desc = models.TextField("Opis książki", max_length=None)
    book_width = models.PositiveIntegerField("Szerokość okładki (w px)", default="200")
    book_height = models.PositiveIntegerField("Wysokość okładki (w px)", default="400")
    book_img = models.ImageField("Okładka książki", width_field='book_width', height_field='book_height', blank=True, null=True, upload_to="covers/%Y/%m/%D/")
    book_author = models.ManyToManyField(Author, verbose_name="Autor/Autorzy")
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria")
    pub_date = models.DateTimeField('Data utworzenia', auto_now_add=True)
    book_likes = models.PositiveIntegerField("Plusy", default=0)
    book_dislikes = models.PositiveIntegerField("Minusy", default=0)
    def __str__(self):
        return self.book_title


class Comment(models.Model):
    content = models.TextField("Treść komentarza", max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    pub_date = models.DateTimeField('Data utworzenia', auto_now_add=True)
    book = models.ForeignKey(Book, verbose_name="Książka", on_delete=models.CASCADE, default=None, blank=True)

    def __str__(self):
        return self.content[:10]

