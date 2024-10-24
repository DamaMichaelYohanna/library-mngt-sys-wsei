from django.db import models

class Author(models.Model):
    full_name = models.CharField(max_length=50)


class Publisher(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    """Database model class for book tables"""
    name = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    isbn = models.CharField(max_length=15)
    copies = models.PositiveIntegerField()
