from django.db import models

class Author(models.Model):
    full_name = models.CharField(max_length=50)


class Publisher(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    """Database model class for book tables"""
    name = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, null=True)
    isbn = models.CharField(max_length=15)
    is_available = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.name}"
    
    def book_detail(self):
        return f'{self.name} published by {self.publisher}'