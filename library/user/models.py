from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    identity = models.PositiveIntegerField()
    book_borrow = models.ManyToManyField(null=True, blank=True)
    has_borrowed = models.BooleanField(default=False)