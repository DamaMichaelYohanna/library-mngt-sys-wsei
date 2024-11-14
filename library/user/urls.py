from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
   
]