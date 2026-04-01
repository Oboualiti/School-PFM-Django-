from django.urls import path
from . import views

urlpatterns = [
 path('', views.student_list, name='student_list'),
 path('add/', views.add_student, name='add_student'),
 path('students/export/', views.export_students_csv, name='export_students_csv'),
 path('students/<str:student_id>/',
 views.view_student, name='view_student'),
 path('edit/<str:student_id>/',
 views.edit_student, name='edit_student'),
 path('delete/<str:student_id>/',
 views.delete_student, name='delete_student'),

 path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
 
 path('profile/<str:student_id>/', views.my_profile , name='my_profile'),

]
