# Generated by Django 3.0.3 on 2020-02-19 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20200219_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_img',
            field=models.ImageField(blank=True, height_field='book_height', null=True, upload_to='covers/%Y/%m/%D/', verbose_name='Okładka książki', width_field='book_width'),
        ),
    ]