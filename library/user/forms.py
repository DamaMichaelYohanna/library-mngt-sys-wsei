from django import forms


class LoginForm(forms.Form):
    """form class for login"""
    username = forms.CharField( widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
