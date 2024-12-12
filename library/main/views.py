from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import BookForm
from .models import Author, Book, Publisher


# Book Management Views
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('name')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        isbn = request.POST.get('isbn')
        stock = request.POST.get('is_available')
        if title and author and publisher and isbn and stock:
            authors_list = []
            if ',' in author:              
                authors = author.split(',')
                for author in authors:
                    if author:
                        author = Author.objects.create(full_name=author)
                        authors_list.append(author)
            else:
                author = Author.objects.create(full_name=author)
                authors_list.append(author)

            publisher = Publisher.objects.create(name=publisher)

            book = Book.objects.create(
                name=title,
                publisher=publisher, isbn=isbn,
            )
            book.is_available=True if stock else False
            for author in authors_list:
                book.author.add(author)
            book.save()
        messages.success(request, "Book added successfully.")
        return redirect('/account/staff_dashboard')
    return render(request, 'main/add_book.html',)

def search_books(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'search_books.html', {'books': books})


def book_list(request):
    """list book in admin site"""
    # Get the search query from the request
    search_query = request.GET.get('search', '')

    # Filter books based on the search query
    if search_query:
        books = Book.objects.filter(
            name__icontains=search_query  # Search by book name
        )
    else:
        books = Book.objects.all()

    # Render the HTML template with the list of books
    return render(request, 'main/book_list.html', {'books': books, 'search_query': search_query})

@login_required
def update_book(request, pk):
    """View to update book from admin site"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # Populate the form with data from the POST request
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()  # Save the updated book to the database
            return redirect('/books')  # Redirect to the book list page
    else:
        # Create a form pre-filled with the book's current data
        form = BookForm(instance=book)

    return render(request, 'main/update_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, pk):
    """View to delete book by admin"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()  # Delete the book from the database
        return redirect('/books')  # Redirect to the book list page

    return render(request, 'main/delete_book.html', {'book': book})
