from django.contrib import admin
from .models import Student, Librarian, Administrator

admin.site.register(Student)
admin.site.register(Librarian)
admin.site.register(Administrator)