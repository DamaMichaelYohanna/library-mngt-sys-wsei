from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from main.models import Book
from user.models import Administrator, Librarian, Student

from .forms import LoginForm, StaffForm, StaffUpdateForm, StudentForm, StudentUpdateForm

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
                return redirect('user:login')

            login(request, user)
            if user.is_superuser:
                return redirect('/account/staff_dashboard')
            elif user.is_staff:
                return redirect("/account/staff_dashboard")
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


def user_list(request):
    # Get search and category filters from GET parameters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    if search_query and category_filter:
        # Filter users based on search query and category
        administrators = Administrator.objects.filter(user__first_name__icontains=search_query) if category_filter in ['', 'administrator'] else []
        librarians = Librarian.objects.filter(user__first_name__icontains=search_query, deleted=False) if category_filter in ['', 'librarian'] else []
        students = Student.objects.filter(user__first_name__icontains=search_query, deleted=False) if category_filter in ['', 'student'] else []
        # Combine all users into one list
        users = list(administrators) + list(librarians) + list(students)
    elif search_query:
        administrators = Administrator.objects.filter(user__first_name__icontains=search_query)
        librarians = Librarian.objects.filter(user__first_name__icontains=search_query, deleted=False)
        students = Student.objects.filter(user__first_name__icontains=search_query, deleted=False)
        # Combine all users into one list
        users = list(administrators) + list(librarians) + list(students)
    elif category_filter:
        if category_filter == 'administrator':
            result = Administrator.objects.all()
        elif category_filter == 'librarian':
            result = Librarian.objects.filter(deleted=False)
        elif category_filter == 'student':
            result = Student.objects.filter(deleted=False)
        # Combine all users into one list
        users = result
    else:
        result1 = Administrator.objects.all()
        result2 = Librarian.objects.filter(deleted=False)
        result3 = Student.objects.filter(deleted=False)
        # Combine all users into one list
        users = list(result1) + list(result2) + list(result3)

    return render(request, 'user/user_list.html', {'users': users})


# -------------------------------------------------------

class StaffCreateView(View):
    """
    View for creating staff model.
    """
    form_class: StaffForm = StaffForm
    template_name: str = 'user/create_staff.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form_data: StaffForm = self.form_class(request.POST)
        if form_data.is_valid():
            staff = form_data.save()
            if staff:
                 messages.success(request, "Staff created successfully!")
                 return redirect('user:user_list')
            else:
                messages.error(request, "An error occurred!")
                return render(request, "user/create_staff", context={"error": "Fields missing"})
            

class StaffUpdateView(View):
    template_name="user/staff_update.html"
    form_class = StaffUpdateForm

    def get(self, request, pk, *args, **kwargs):
        librarian = get_object_or_404(Librarian, pk=pk)
        initial_data = {
        "first_name": librarian.user.first_name,
        "last_name": librarian.user.last_name,
        "email": librarian.user.email,
        "role": librarian.role,
        "phone": librarian.phone
    }
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        librarian = get_object_or_404(Librarian, pk=pk)
        form_data: StaffUpdateForm = self.form_class(request.POST)
        if form_data.is_valid():
            form_data = form_data.cleaned_data
            librarian.first_name = form_data.get('first_name', librarian.user.first_name)
            librarian.last_name = form_data.get('last_name',librarian.user.last_name)
            librarian.user.email = form_data.get('email', librarian.user.email),
            librarian.phone = form_data.get("phone", librarian.phone)
            librarian.role = form_data.get("role", librarian.role)
            librarian.save()
            messages.error(request, "Staff updated successfully")
            return redirect("user:user_list")
   
class StaffDeleteView(View):
     
     def get(self, request, pk, *args, **kwargs):
        librarian = get_object_or_404(Librarian, pk=pk)
        librarian.deleted = True
        librarian.save()
        messages.error(request, "Staff deleted successfully")
        return redirect("user:user_list")
             
#---------------------------------------------------------------

class StudentCreateView(View):
    """
    View for creating staff model.
    """
    form_class: StaffForm = StudentForm
    template_name: str = 'user/create_staff.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form_data: StudentForm = self.form_class(request.POST)
        if form_data.is_valid():
            student = form_data.save()
            if student:
                 messages.success(request, "Student created successfully!")
                 return redirect('user:user_list')
            else:
                messages.error(request, "An error occurred!")
                return render(request, "user/create_staff", context={"error": "Fields missing"})
        else:
            return render(request, self.template_name, {"form": form_data})
            

class StudentUpdateView(View):
    template_name="user/staff_update.html"
    form_class = StudentUpdateForm

    def get(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, pk=pk)
        initial_data = {
        "first_name": student.user.first_name,
        "last_name": student.user.last_name,
        "email": student.user.email,
    }
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form_data: StudentUpdateForm = self.form_class(request.POST)
        if form_data.is_valid():
            form_data = form_data.cleaned_data
            print(form_data)
            student.user.first_name = form_data.get('first_name', student.user.first_name)
            student.user.last_name = form_data.get('last_name',student.user.last_name)
            student.user.email = form_data.get('email', student.user.email),
            student.save()
            messages.error(request, "Student updated successfully")
            return redirect("user:user_list")
        return render(request, self.template_name, {"form": form_data})
   
class StudentDeleteView(View):
     
     def get(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, pk=pk)
        student.deleted = True
        student.save()
        messages.error(request, "Student deleted successfully")
        return redirect("user:user_list")
             




