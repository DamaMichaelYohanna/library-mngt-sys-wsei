from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path("staff/create", views.StaffCreateView.as_view(), name="create_staff"),
    path("staff/update/<int:pk>", views.StaffUpdateView.as_view(), name="update_staff"),
    path("staff/delete/<int:pk>", views.StaffDeleteView.as_view(), name="delete_staff"),
    path("staff/create/student", views.StudentCreateView.as_view(), name="create_student"),
    path("staff/update/<int:pk>/student", views.StudentUpdateView.as_view(), name="update_student"),
    path("staff/delete/<int:pk>/student", views.StudentDeleteView.as_view(), name="delete_student"),
    path('users/', views.user_list, name='user_list'),
    # path('users/update/<int:pk>/', update_user, name='update_user'),
    # path('users/delete/<int:pk>/', delete_user, name='delete_user'),
   
]