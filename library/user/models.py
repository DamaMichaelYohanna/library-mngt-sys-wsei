from django.db import models
from django.contrib.auth import get_user_model

from main.models import Book


User = get_user_model()  # get the django default user model 
class Administrator(models.Model):
    """Database model for Administrator's account. will inherit from the django
    User model which has other fields like first and last name, email, password, and rank"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    def __str__(self):
        return f'{self.user}'



class Librarian(models.Model):
    """Database model for Librarian's account. will inherit from the django
    User model which has other fields like first and last name, email, password, and rank"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    role = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'



class Student(models.Model):
    """Database model for Student account. will inherit from the django
    User model which has other fields like first and last name, email, password,"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_borrow = models.ManyToManyField(Book, blank=True)
    has_borrowed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    role = models.CharField(max_length=7, default="Student")


    def __str__(self):
        return f'{self.user}'


