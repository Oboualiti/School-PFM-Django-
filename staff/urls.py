from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/<int:teacher_id>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teachers/<int:teacher_id>/delete/', views.delete_teacher, name='delete_teacher'),
    path('teacher_profile/<int:teacher_id>/', views.teacher_profile , name='teacher_profile'),
]

