# academic/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.utils.dateparse import parse_datetime
import json

from .models import Grade, Exam, Subject, Holiday, Department, SubjectProposal, ExamQuestion
from student.models import Student
from staff.models import Teacher


def get_teacher_from_request(request):
    """
    Utility function to get teacher profile from request user.
    Returns (teacher, error_response) tuple where error_response is None if successful.
    """
    if not request.user.is_authenticated:
        return None, JsonResponse({'error': 'Authentication required'}, status=401)
    
    if not request.user.is_teacher:
        return None, JsonResponse({'error': 'Forbidden: teacher access required'}, status=403)
    
    try:
        teacher = Teacher.objects.get(user=request.user)
        return teacher, None
    except Teacher.DoesNotExist:
        return None, JsonResponse({'error': 'Teacher profile not found'}, status=403)

# --- GESTION DES DÉPARTEMENTS (DEPARTMENTS) ---

@login_required
def department_list(request):
    """Display list of all departments"""
    departments = Department.objects.all().select_related('head_of_dept')
    return render(request, 'academic/departments.html', {'departments': departments})

@login_required
def add_department(request):
    """Add a new department"""
    if not request.user.is_admin:
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        name = request.POST.get('name')
        head_of_dept_id = request.POST.get('head_of_dept')
        
        dept_data = {'name': name}
        if head_of_dept_id:
            dept_data['head_of_dept_id'] = head_of_dept_id
        
        Department.objects.create(**dept_data)
        messages.success(request, 'Department created successfully')
        return redirect('department_list')
    
    teachers = Teacher.objects.all()
    return render(request, 'academic/add-department.html', {'teachers': teachers})

@login_required
def edit_department(request, dept_id):
    """Edit department details"""
    if not request.user.is_admin:
        return HttpResponseForbidden("Access denied.")
    
    department = get_object_or_404(Department, id=dept_id)
    
    if request.method == 'POST':
        department.name = request.POST.get('name')
        head_of_dept_id = request.POST.get('head_of_dept')
        if head_of_dept_id:
            department.head_of_dept_id = head_of_dept_id
        department.save()
        messages.success(request, 'Department updated successfully')
        return redirect('department_list')
    
    teachers = Teacher.objects.all()
    return render(request, 'academic/edit-department.html', {
        'department': department,
        'teachers': teachers
    })

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
    ctx = {'exams': exams}
    if request.user.is_authenticated and getattr(request.user, 'is_teacher', False):
        # Limit subjects to those owned by this teacher
        my_subjects = Subject.objects.filter(teacher__user_id=request.user.id)
        ctx['subjects'] = my_subjects
    return render(request, 'academic/exams.html', ctx)

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

@login_required
def add_exam_teacher(request):
    """Teacher-specific exam creation view that only shows their subjects"""
    if not request.user.is_teacher:
        return HttpResponseForbidden("Only teachers can access this page.")
    
    # Get the teacher profile for the current user
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return HttpResponseForbidden("Teacher profile not found. Please contact administrator.")
    
    # Only show subjects assigned to this teacher
    subjects = Subject.objects.filter(teacher=teacher)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        
        # Verify the subject belongs to this teacher
        subject_obj = get_object_or_404(Subject, id=subject_id, teacher=teacher)
        
        Exam.objects.create(
            name=name,
            subject=subject_obj,
            date=date
        )
        messages.success(request, 'Exam created successfully!')
        return redirect('exam_list')
    
    return render(request, 'academic/add-exam-teacher.html', {'subjects': subjects})

@csrf_protect
def create_exam_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Validate teacher authentication and profile
    teacher, error_response = get_teacher_from_request(request)
    if error_response:
        return error_response
    try:
        if request.content_type and 'application/json' in request.content_type:
            payload = json.loads(request.body.decode('utf-8'))
        else:
            payload = request.POST
        title = payload.get('title') or payload.get('name')
        description = payload.get('description', '')
        subject_id = payload.get('subject')
        start_dt = payload.get('start_datetime')
        end_dt = payload.get('end_datetime')
        questions = payload.get('questions', [])

        if not title or not subject_id or not start_dt or not end_dt:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        subject = get_object_or_404(Subject, id=subject_id)
        # Verify teacher owns subject
        if not subject.teacher or subject.teacher.user_id != request.user.id:
            return JsonResponse({'error': 'Forbidden: not assigned to subject'}, status=403)
        start_parsed = parse_datetime(start_dt)
        end_parsed = parse_datetime(end_dt)
        if not start_parsed or not end_parsed:
            return JsonResponse({'error': 'Invalid datetime format'}, status=400)
        if end_parsed <= start_parsed:
            return JsonResponse({'error': 'End must be after start'}, status=400)
        if isinstance(questions, str):
            try:
                questions = json.loads(questions)
            except Exception:
                questions = []
        if not isinstance(questions, list):
            return JsonResponse({'error': 'Questions must be a list'}, status=400)

        with transaction.atomic():
            exam = Exam.objects.create(
                name=title,
                description=description,
                subject=subject,
                date=start_parsed.date(),
                start_datetime=start_parsed,
                end_datetime=end_parsed
            )
            for q in questions:
                if isinstance(q, dict):
                    text = q.get('text')
                    marks = q.get('marks')
                else:
                    text = str(q)
                    marks = None
                if not text:
                    transaction.set_rollback(True)
                    return JsonResponse({'error': 'Question text required'}, status=400)
                ExamQuestion.objects.create(exam=exam, text=text, marks=marks)
        return JsonResponse({'id': exam.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error', 'details': str(e)}, status=500)

# --- GESTION DES MATIÈRES (SUBJECTS) ---

def subject_list(request):
    subjects = Subject.objects.all().select_related('department', 'teacher')
    return render(request, 'academic/subjects.html', {'subjects': subjects})

@login_required
def add_subject(request):
    if not (request.user.is_admin or request.user.is_teacher):
        return HttpResponseForbidden()

    if request.method == 'POST':
        name = request.POST.get('name')
        dept_id = request.POST.get('department')
        dept_obj = get_object_or_404(Department, id=dept_id)
        
        # If the requester is a teacher, automatically link the subject to their teacher profile
        if request.user.is_teacher:
            try:
                teacher_obj = Teacher.objects.get(user=request.user)
            except Teacher.DoesNotExist:
                return HttpResponseForbidden("Teacher profile not found. Please contact administrator.")
        else:
            # Admin can assign any teacher
            teacher_id = request.POST.get('teacher')
            teacher_obj = get_object_or_404(Teacher, id=teacher_id)

        Subject.objects.create(
            name=name,
            department=dept_obj,
            teacher=teacher_obj
        )
        messages.success(request, 'Subject created successfully!')
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
        return HttpResponseForbidden("Only administrators can manage holidays.")

    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('holiday_date')
        h_type = request.POST.get('type')
        description = request.POST.get('description', '')

        if not name or not date or not h_type:
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'academic/add-holiday.html')

        # Check for duplicates or overlapping dates
        if Holiday.objects.filter(holiday_date=date).exists():
            messages.error(request, f'A holiday already exists on {date}.')
            return render(request, 'academic/add-holiday.html')

        Holiday.objects.create(
            name=name,
            holiday_date=date,
            type=h_type,
            description=description
        )
        messages.success(request, 'Holiday added successfully!')
        return redirect('holiday_list')

    return render(request, 'academic/add-holiday.html')

@login_required
def delete_holiday(request, holiday_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only administrators can manage holidays.")
    
    if request.method == 'POST':
        holiday = get_object_or_404(Holiday, id=holiday_id)
        holiday.delete()
        messages.success(request, 'Holiday deleted successfully!')
        
    return redirect('holiday_list')

@login_required
def proposal_list(request):
    if request.user.is_admin or request.user.is_teacher:
        proposals = SubjectProposal.objects.all().select_related('department', 'proposer')
    else:
        proposals = SubjectProposal.objects.filter(proposer=request.user).select_related('department', 'proposer')
    return render(request, 'academic/proposals.html', {'proposals': proposals})

@login_required
def add_proposal(request):
    if not request.user.is_student:
        return HttpResponseForbidden()
    if request.method == 'POST':
        name = request.POST.get('name')
        dept_id = request.POST.get('department')
        description = request.POST.get('description', '')
        dept_obj = get_object_or_404(Department, id=dept_id)
        SubjectProposal.objects.create(
            name=name,
            department=dept_obj,
            proposer=request.user,
            description=description
        )
        messages.success(request, 'Proposal submitted')
        return redirect('proposal_list')
    departments = Department.objects.all()
    return render(request, 'academic/add-proposal.html', {'departments': departments})

@login_required
def approve_proposal(request, id):
    if not (request.user.is_admin or request.user.is_teacher):
        return HttpResponseForbidden()
    prop = get_object_or_404(SubjectProposal, id=id)
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        teacher_obj = get_object_or_404(Teacher, id=teacher_id)
        Subject.objects.create(
            name=prop.name,
            department=prop.department,
            teacher=teacher_obj
        )
        prop.status = 'approved'
        prop.save()
        messages.success(request, 'Proposal approved')
        return redirect('proposal_list')
    teachers = Teacher.objects.all()
    return render(request, 'academic/approve-proposal.html', {'proposal': prop, 'teachers': teachers})

@login_required
def reject_proposal(request, id):
    if not (request.user.is_admin or request.user.is_teacher):
        return HttpResponseForbidden()
    prop = get_object_or_404(SubjectProposal, id=id)
    prop.status = 'rejected'
    prop.save()
    messages.success(request, 'Proposal rejected')
    return redirect('proposal_list')
