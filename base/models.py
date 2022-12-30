
from asyncio.windows_events import NULL
from tkinter import CASCADE

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    book1 = models.CharField(max_length=100, default="no")
    book2 = models.CharField(max_length=100, default="no")


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    
    copies = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True)
    coverpage = models.TextField()

