# Generated by Django 3.0.3 on 2020-02-18 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Autor')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, verbose_name='Kategoria')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, verbose_name='Treść komentarza')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=50, verbose_name='Tytuł książki')),
                ('book_desc', models.TextField(verbose_name='Opis książki')),
                ('book_img', models.ImageField(blank=True, null=True, upload_to='covers/%Y/%m/%D/', verbose_name='Okładka książki')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('book_likes', models.IntegerField(default=0, verbose_name='Ocena')),
                ('book_author', models.ManyToManyField(to='books.Author', verbose_name='Autor/Autorzy')),
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Category', verbose_name='Kategoria')),
                ('comments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Comment', verbose_name='Komentarze')),
            ],
        ),
    ]
