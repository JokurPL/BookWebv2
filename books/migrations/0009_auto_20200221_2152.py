# Generated by Django 3.0.3 on 2020-02-21 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20200220_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.TextField(max_length=25, verbose_name='Użytkownik'),
        ),
    ]
