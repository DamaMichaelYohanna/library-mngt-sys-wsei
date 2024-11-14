from django.shortcuts import redirect, render
from django.contrib import messages
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
