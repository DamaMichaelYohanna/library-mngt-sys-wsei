from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from main.models import Book
from user.models import Student

from .forms import LoginForm

def logout_view(request):
    logout(request)  # logout the current session
    return redirect('/account/login')

class LoginView(View):
    form_class: LoginForm = LoginForm
    template_name: str = 'user/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_data: LoginForm = self.form_class(request.POST)
        if form_data.is_valid():
            username: str = form_data.cleaned_data['username']
            password: str = form_data.cleaned_data['password']
            user: User | None = authenticate(username=username, password=password)
            if not user:
                messages.error(request, 'Wrong login details!')
                return redirect('login')

            login(request, user)
            if user.is_superuser:
                return redirect('admin')
            elif user.is_staff:
                return redirect("librarian")
            else:
                return redirect('/account/student_dashboard')
            
def student_dashboard(request):
    if request.method == 'POST':
        # Handle book borrowing from the form
        book_id = request.POST.get('book_id')
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            if not book.is_available:
                book.save()
                student.book_borrow.add(book)
                student.has_borrowed = True
                student.save()
        return redirect('/account/student_dashboard')
    student = get_object_or_404(Student, user=request.user)
    books = Book.objects.filter(is_available=True)
    borrowed_books = student.book_borrow.all()
    context ={"student": student, 'available_books': books, 'borrowed_books': borrowed_books}
    return render(request, 'user/student_dashboard.html', context)

def staff_dashboard(request):
    return render(request, 'user/staff_dashboard.html')
