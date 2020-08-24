from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.html import format_html
from django.urls import reverse


# Create your models here.

class Author(models.Model):
    name = models.CharField("Autor", max_length=50)
    description = models.TextField("Opis autora", max_length=None, default="Brak opisu")

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField("Kategoria", max_length=50)

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'

    def __str__(self):
        return self.category_name


class Book(models.Model):
    book_title = models.CharField("Tytuł książki", max_length=50)
    book_desc = models.TextField("Opis książki", max_length=None)
    book_width = models.PositiveIntegerField("Szerokość okładki (w px)", default="200")
    book_height = models.PositiveIntegerField("Wysokość okładki (w px)", default="400")
    book_img = models.ImageField("Okładka książki", width_field='book_width', height_field='book_height', blank=True,
                                 null=True, upload_to="covers/%Y/%m/%D/")
    book_author = models.ManyToManyField(Author, verbose_name="Autor/Autorzy")
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria")
    pub_date = models.DateTimeField('Data utworzenia', auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Opening the uploaded image
        try:
            im = Image.open(self.book_img).convert('RGB')

            output = BytesIO()

            IM_RESIZE = im.resize((350, 490))

            # Resize/modify the image
            im = IM_RESIZE

            # after modifications, save it to the output
            im.save(output, format='JPEG', quality=100)
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.book_img = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.book_img.name.split('.')[0],
                                                 'image/jpeg', sys.getsizeof(output), None)

            super(Book, self).save()
        except ValueError:
            super(Book, self).save()

    class Meta:
        verbose_name = 'Książkę'
        verbose_name_plural = 'Książki'

    def __str__(self):
        return self.book_title


class Comment(models.Model):
    content = models.TextField("Treść komentarza", max_length=500)
    user = models.ForeignKey(User, verbose_name="Użytkownik", on_delete=models.CASCADE, default=None, blank=True)
    pub_date = models.DateTimeField('Data utworzenia', auto_now_add=True)
    book = models.ForeignKey(Book, verbose_name="Książka", on_delete=models.CASCADE, default=None, blank=True)

    class Meta:
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'

    def __str__(self):
        return self.content[:10]


class Rating(models.Model):
    like = models.BooleanField("Like")
    dislike = models.BooleanField("Dislike")
    user = models.ForeignKey(User, verbose_name="Użytkownik", on_delete=models.CASCADE, default=None, blank=True)
    book = models.ForeignKey(Book, verbose_name="Książka", on_delete=models.CASCADE, default=None, blank=True)

    class Meta:
        verbose_name = 'Ocena'
        verbose_name_plural = 'Oceny'

    def __str__(self):
        return "Ocena dla: " + self.book.book_title
