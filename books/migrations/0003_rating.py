# Generated by Django 3.0.3 on 2020-06-10 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_auto_20200609_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(verbose_name='Like')),
                ('dislike', models.BooleanField(verbose_name='Dislike')),
                ('book', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='books.Book', verbose_name='Książka')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
        ),
    ]