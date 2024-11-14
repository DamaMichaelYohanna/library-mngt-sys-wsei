 


from django.urls import path

from . import views

urlpatterns = [
    path('add_book/', views.add_book, name='add_book'),
    path('search_books/', views.search_books, name='search_books'),
   
]