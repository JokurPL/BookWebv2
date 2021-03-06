# Generated by Django 3.0.3 on 2020-06-09 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='comments',
        ),
        migrations.AddField(
            model_name='book',
            name='book_dislikes',
            field=models.PositiveIntegerField(default=0, verbose_name='Minusy'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_height',
            field=models.PositiveIntegerField(default='400', verbose_name='Wysokość okładki (w px)'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_width',
            field=models.PositiveIntegerField(default='200', verbose_name='Szerokość okładki (w px)'),
        ),
        migrations.AddField(
            model_name='comment',
            name='book',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='books.Book', verbose_name='Książka'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_img',
            field=models.ImageField(blank=True, height_field='book_height', null=True, upload_to='covers/%Y/%m/%D/', verbose_name='Okładka książki', width_field='book_width'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Plusy'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
    ]
