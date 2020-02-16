from django.db import models

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
    book_img = models.ImageField("Okładka książki", blank=True, null=True, upload_to="covers/%Y/%m/%D/")
    book_author = models.ManyToManyField(Author, verbose_name="Autor/Autorzy")
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria")
    pub_date = models.DateTimeField('date published')
    book_likes = models.IntegerField("Ocena", default=0)
    def __str__(self):
        return self.book_title



