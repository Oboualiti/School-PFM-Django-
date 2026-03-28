from django.urls import path
from . import views

urlpatterns = [
    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/<int:dept_id>/edit/', views.edit_department, name='edit_department'),
    
    # Subject URLs
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    
    # Exam URLs
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/teacher/add/', views.add_exam_teacher, name='add_exam_teacher'),
    path('exams/create/', views.create_exam_api, name='create_exam_api'),
    
    # Grade URLs
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/add/', views.add_grade, name='add_grade'),
    
    # Holiday URLs
    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.add_holiday, name='add_holiday'),
    path('holidays/<int:holiday_id>/delete/', views.delete_holiday, name='delete_holiday'),
    
    # Proposal URLs
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposals/add/', views.add_proposal, name='add_proposal'),
    path('proposals/<int:id>/approve/', views.approve_proposal, name='approve_proposal'),
    path('proposals/<int:id>/reject/', views.reject_proposal, name='reject_proposal'),
]

