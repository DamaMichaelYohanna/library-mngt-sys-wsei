 


from django.urls import path

from . import views

urlpatterns = [
    path('add_book/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('books/update/<int:pk>/', views.update_book, name='update_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('search_books/', views.search_books, name='search_books'),
   
]