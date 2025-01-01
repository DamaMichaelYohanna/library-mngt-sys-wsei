 


from django.urls import path

from . import views
from user.views import LoginView
app_name = 'main'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('books/update/<int:pk>/', views.update_book, name='update_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('search_books/', views.search_books, name='search_books'),
    path("books/borrow/<int:pk>/", views.borrow_book, name="borrow_book"),
    path("books/borrowers/", views.borrower_list, name="borrowers"),
    path("books/return/<int:book_id>/<int:student_id>", views.return_book, name="borrowers"),

   
]