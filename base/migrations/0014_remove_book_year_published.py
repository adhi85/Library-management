# Generated by Django 4.1.2 on 2022-10-17 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_book_year_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='year_published',
        ),
    ]
