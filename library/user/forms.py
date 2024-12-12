from django import forms
from django.contrib.auth.models import User
from .models import Librarian, Student 


class LoginForm(forms.Form):
    """form class for login"""
    username = forms.CharField( widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class StaffForm(forms.ModelForm):
    """form for adding new staff record"""
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    
    class Meta:
        model = Librarian
        fields = ['phone', 'role']
        widgets = {
            'role': forms.TextInput(attrs={'placeholder': 'Enter the role'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter a valid phone number'}),
        }

    def save(self, commit=True):
        # Create the user instance
        user_data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],
            'username': self.cleaned_data['email'],  # Username set as email
            "is_staff": True
        }
        user = User(**user_data)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()

        librarian = super().save(commit=False)
        librarian.user = user  # Assign the created user to the librarian
        if commit:
            librarian.save()
        return librarian
    

class StaffUpdateForm(forms.ModelForm):
    """form for updating staff record"""
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    
    class Meta:
        model = Librarian
        fields = ['phone', 'role']
        widgets = {
            'role': forms.TextInput(attrs={'placeholder': 'Enter the role'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter a valid phone number'}),
        }


class StudentForm(forms.Form):
    """form for registering new student"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter first name"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter last name"})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"})
    )
    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )
    

    def save(self, commit=True):
        # Create the user instance
        user_data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],
            'username': self.cleaned_data['email'],  # Username set as email
        }
        user = User(**user_data)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()

        student = Student.objects.create(user=user)
        student.save()
        return student
    

class StudentUpdateForm(forms.Form):
    """form for updating student record"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter first name"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter last name"})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"})
    )
