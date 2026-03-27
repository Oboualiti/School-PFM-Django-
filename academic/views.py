# academic/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Grade, Exam, Subject, Holiday, Department
from student.models import Student
from staff.models import Teacher

# --- GESTION DES NOTES (GRADES) ---

@login_required
def add_grade(request):
    # Seuls Admin et Enseignants peuvent saisir des notes
    if not (request.user.is_admin or request.user.is_teacher):
        return HttpResponseForbidden("Accès refusé.")

    if request.method == 'POST':
        student_id = request.POST.get('student')
        exam_id = request.POST.get('exam')
        mark = request.POST.get('mark')

        # Récupération sécurisée des objets
        student_obj = get_object_or_404(Student, id=student_id)
        exam_obj = get_object_or_404(Exam, id=exam_id)

        # Création de la note en base de données
        Grade.objects.create(
            student=student_obj,
            exam=exam_obj,
            mark=float(mark)
        )

        messages.success(request, 'Note ajoutée avec succès !')
        return redirect('grade_list')

    # Données pour remplir les menus déroulants du formulaire
    students = Student.objects.all()
    exams = Exam.objects.all()
    return render(request, 'academic/add-grade.html', {
        'students': students, 
        'exams': exams
    })

def grade_list(request):
    # .select_related permet d'optimiser la requête SQL
    grades = Grade.objects.all().select_related('student', 'exam')
    return render(request, 'academic/grades.html', {'grades': grades})


# --- GESTION DES EXAMENS (EXAMS) ---

def exam_list(request):
    exams = Exam.objects.all().select_related('subject')
    return render(request, 'academic/exams.html', {'exams': exams})

@login_required
def add_exam(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Réservé à l'administration.")

    if request.method == 'POST':
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')

        subject_obj = get_object_or_404(Subject, id=subject_id)

        Exam.objects.create(
            name=name,
            subject=subject_obj,
            date=date
        )
        messages.success(request, 'Examen planifié avec succès !')
        return redirect('exam_list')

    subjects = Subject.objects.all()
    return render(request, 'academic/add-exam.html', {'subjects': subjects})


# --- GESTION DES MATIÈRES (SUBJECTS) ---

def subject_list(request):
    subjects = Subject.objects.all().select_related('department', 'teacher')
    return render(request, 'academic/subjects.html', {'subjects': subjects})

@login_required
def add_subject(request):
    if not request.user.is_admin:
        return HttpResponseForbidden()

    if request.method == 'POST':
        name = request.POST.get('name')
        dept_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')

        dept_obj = get_object_or_404(Department, id=dept_id)
        teacher_obj = get_object_or_404(Teacher, id=teacher_id)

        Subject.objects.create(
            name=name,
            department=dept_obj,
            teacher=teacher_obj
        )
        messages.success(request, 'Matière créée !')
        return redirect('subject_list')

    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'academic/add-subject.html', {
        'departments': departments,
        'teachers': teachers
    })


# --- GESTION DES JOURS FÉRIÉS (HOLIDAYS) ---

def holiday_list(request):
    holidays = Holiday.objects.all().order_by('holiday_date')
    return render(request, 'academic/holidays.html', {'holidays': holidays})

@login_required
def add_holiday(request):
    if not request.user.is_admin:
        return HttpResponseForbidden()

    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('holiday_date')
        h_type = request.POST.get('type')

        Holiday.objects.create(
            name=name,
            holiday_date=date,
            type=h_type
        )
        messages.success(request, 'Jour férié ajouté !')
        return redirect('holiday_list')

    return render(request, 'academic/add-holiday.html')