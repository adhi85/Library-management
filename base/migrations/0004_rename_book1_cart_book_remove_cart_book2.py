# Generated by Django 4.1.2 on 2022-10-13 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_cart_remove_user_book1_remove_user_book2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='book1',
            new_name='book',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='book2',
        ),
    ]
