# academic/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.db.models import Avg, Max, Min, Q, Count
from django.utils.dateparse import parse_datetime
import json
from .models import Class
from .models import Grade, Exam, Subject, Holiday, Department, SubjectProposal, ExamQuestion
from student.models import Student
from staff.models import Teacher


def get_teacher_from_request(request):
    if not request.user.is_authenticated:
        return None, JsonResponse({'error': 'Authentication required'}, status=401)
    
    if not request.user.is_teacher:
        return None, JsonResponse({'error': 'Forbidden: teacher access required'}, status=403)
    
    try:
        teacher = Teacher.objects.get(user=request.user)
        return teacher, None
    except Teacher.DoesNotExist:
        return None, JsonResponse({'error': 'Teacher profile not found'}, status=403)

# --- DEPARTMENTS ---

@login_required
def department_list(request):
    departments = Department.objects.all().select_related('head_of_dept')
    return render(request, 'academic/departments.html', {'departments': departments})

@login_required
def add_department(request):
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

@login_required    
def delete_department(request, dept_id):
    if request.method == "POST":
        department = get_object_or_404(Department, id=dept_id)
        department.delete()
        messages.success(request, "Department deleted successfully!")
    return redirect('department_list')

@login_required
def add_grade(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden("Only teachers can add grades.")

    teacher = get_object_or_404(Teacher, user=request.user)
    
    exam_id = request.GET.get('exam_id') or request.POST.get('exam_id')
    exam = get_object_or_404(Exam, id=exam_id)
    
    if exam.subject.teacher != teacher:
        return HttpResponseForbidden("You are not the teacher for this exam's subject.")

    students = Student.objects.filter(student_class=exam.class_group)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        mark = request.POST.get('mark')

        student = get_object_or_404(students, id=student_id)

        Grade.objects.update_or_create(
            student=student, 
            exam=exam, 
            defaults={'mark': mark}
        )
        
        messages.success(request, f"Grade for {student} updated successfully!")
        return redirect('grade_list')

    return render(request, 'academic/add-grade.html', {
        'exam': exam,
        'students': students
    })
# --- GRADES ---

@login_required
def grade_list(request):
    search_query = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if request.user.is_admin:
        grades = Grade.objects.all().select_related('student', 'exam', 'exam__subject')
    elif request.user.is_teacher:
        teacher = get_object_or_404(Teacher, user=request.user)
        grades = Grade.objects.filter(exam__subject__teacher=teacher).select_related('student', 'exam', 'exam__subject')
    elif request.user.is_student:
        student = get_object_or_404(Student, user=request.user)
        grades = Grade.objects.filter(student=student).select_related('exam', 'exam__subject')
    else:
        return HttpResponseForbidden()

    if search_query:
        grades = grades.filter(
            Q(student__first_name__icontains=search_query) | 
            Q(student__last_name__icontains=search_query) |
            Q(exam__name__icontains=search_query)
        )
    if subject_filter:
        grades = grades.filter(exam__subject_id=subject_filter)
    if date_from:
        grades = grades.filter(exam__date__gte=date_from)
    if date_to:
        grades = grades.filter(exam__date__lte=date_to)

    ctx = {
        'grades': grades, 
        'search_query': search_query,
        'subject_filter': subject_filter,
        'date_from': date_from,
        'date_to': date_to
    }

    if request.user.is_admin or request.user.is_teacher:
        ctx['subjects'] = Subject.objects.all() if request.user.is_admin else Subject.objects.filter(teacher__user=request.user)
    
    if request.user.is_student:
        stats = grades.aggregate(
            avg_mark=Avg('mark'),
            max_mark=Max('mark'),
            min_mark=Min('mark'),
            total_exams=Count('id')
        )
        # Ensure default values for stats to avoid template errors
        stats = {
            'avg_mark': stats['avg_mark'] or 0,
            'max_mark': stats['max_mark'] or 0,
            'min_mark': stats['min_mark'] or 0,
            'total_exams': stats['total_exams'] or 0,
        }
        ctx['stats'] = stats
        chart_data = list(reversed(grades.order_by('-exam__date')[:5]))
        ctx['chart_labels'] = [g.exam.name for g in chart_data]
        ctx['chart_values'] = [g.mark for g in chart_data]

    return render(request, 'academic/results.html', ctx)


# --- EXAMS ---

def exam_list(request):
    exams = Exam.objects.all().select_related('subject', 'class_group')
    ctx = {'exams': exams}
    if request.user.is_authenticated and getattr(request.user, 'is_teacher', False):
        my_subjects = Subject.objects.filter(teacher__user_id=request.user.id)
        ctx['subjects'] = my_subjects
        ctx['classes'] = Class.objects.all()
    return render(request, 'academic/exams.html', ctx)

@login_required
def add_exam(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        class_id = request.POST.get('class_group')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        subject_obj = get_object_or_404(Subject, id=subject_id)
        class_group = get_object_or_404(Class, id=class_id)

        from django.utils.dateparse import parse_datetime
        from datetime import datetime
        
        start_dt = None
        end_dt = None
        if date and start_time:
            start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        if date and end_time:
            end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        Exam.objects.create(
            name=name,
            subject=subject_obj,
            class_group=class_group,
            date=date,
            start_datetime=start_dt,
            end_datetime=end_dt
        )
        messages.success(request, 'Exam scheduled successfully!')
        return redirect('exam_list')

    subjects = Subject.objects.all()
    classes = Class.objects.all()
    return render(request, 'academic/add-exam.html', {'subjects': subjects, 'classes': classes})

@login_required
def add_exam_teacher(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden()

    teacher = get_object_or_404(Teacher, user=request.user)

    subjects = Subject.objects.filter(teacher=teacher)
    classes = Class.objects.filter(
        department__in=subjects.values_list('department', flat=True)
    )

    if request.method == 'POST':
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        class_id = request.POST.get('class_group')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        subject = get_object_or_404(Subject, id=subject_id, teacher=teacher)
        class_group = get_object_or_404(Class, id=class_id)

        from datetime import datetime
        start_dt = None
        end_dt = None
        if date and start_time:
            start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        if date and end_time:
            end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        Exam.objects.create(
            name=name,
            subject=subject,
            class_group=class_group,
            date=date,
            start_datetime=start_dt,
            end_datetime=end_dt
        )

        return redirect('exam_list')

    return render(request, 'academic/add-exam-teacher.html', {
        'subjects': subjects,
        'classes': classes
    })

@login_required
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check permissions: admin or the teacher who owns the subject
    if not (request.user.is_admin or (request.user.is_teacher and exam.subject.teacher.user == request.user)):
        return HttpResponseForbidden("You don't have permission to edit this exam.")

    if request.method == 'POST':
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        class_id = request.POST.get('class_group')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        exam.name = name
        exam.subject = get_object_or_404(Subject, id=subject_id)
        exam.class_group = get_object_or_404(Class, id=class_id)
        exam.date = date

        from datetime import datetime
        if date and start_time:
            exam.start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        if date and end_time:
            exam.end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
        
        exam.save()
        
        messages.success(request, 'Exam updated successfully!')
        return redirect('exam_list')

    if request.user.is_admin:
        subjects = Subject.objects.all()
        classes = Class.objects.all()
    else:
        teacher = get_object_or_404(Teacher, user=request.user)
        subjects = Subject.objects.filter(teacher=teacher)
        classes = Class.objects.filter(department__in=subjects.values_list('department', flat=True))

    return render(request, 'academic/edit-exam.html', {
        'exam': exam,
        'subjects': subjects,
        'classes': classes
    })

@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check permissions: admin or the teacher who owns the subject
    if not (request.user.is_admin or (request.user.is_teacher and exam.subject.teacher.user == request.user)):
        return HttpResponseForbidden("You don't have permission to delete this exam.")
    
    exam.delete()
    messages.success(request, 'Exam deleted successfully!')
    return redirect('exam_list')

@csrf_protect
def create_exam_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
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
        class_id = payload.get('class_group')
        start_dt = payload.get('start_datetime')
        end_dt = payload.get('end_datetime')
        questions = payload.get('questions', [])

        if not title or not subject_id or not class_id or not start_dt or not end_dt:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        subject = get_object_or_404(Subject, id=subject_id)
        class_group = get_object_or_404(Class, id=class_id)
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
                class_group=class_group,
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


# --- SUBJECTS ---

def subject_list(request):
    dept_id = request.GET.get('department')
    subjects = Subject.objects.all().select_related('department', 'teacher')
    
    if dept_id:
        subjects = subjects.filter(department_id=dept_id)
        
    departments = Department.objects.all()
    
    return render(request, 'academic/subjects.html', {
        'subjects': subjects,
        'departments': departments,
        'selected_dept': dept_id
    })

@login_required
def add_subject(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admin can add subjects.")

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

        messages.success(request, 'Subject created successfully!')
        return redirect('subject_list')

    departments = Department.objects.all()
    teachers = Teacher.objects.all()

    return render(request, 'academic/add-subject.html', {
        'departments': departments,
        'teachers': teachers
    })

@login_required
def edit_subject(request, subject_id):
    if not request.user.is_admin:
        return redirect('login')

    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.department_id = request.POST.get('department')
        subject.teacher_id = request.POST.get('teacher')
        subject.save()

        messages.success(request, "Subject updated successfully!")
        return redirect('subject_list')

    departments = Department.objects.all()
    teachers = Teacher.objects.all()

    return render(request, 'academic/edit-subject.html', {
        'subject': subject,
        'departments': departments,
        'teachers': teachers
    })

@login_required
def delete_subject(request, subject_id):
    if not request.user.is_admin:
        return HttpResponseForbidden()

    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()

    messages.success(request, "Subject deleted!")
    return redirect('subject_list')
# --- HOLIDAYS ---

def holiday_list(request):
    holidays = Holiday.objects.all().order_by('holiday_date')
    
    calendar_events = []
    for h in holidays:
        calendar_events.append({
            'startDate': h.holiday_date.isoformat(),
            'endDate': h.holiday_date.isoformat(),
            'summary': h.name
        })
        
    return render(request, 'academic/holidays.html', {
        'holidays': holidays,
        'calendar_events': json.dumps(calendar_events)
    })

@login_required
def add_holiday(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only administrators can manage holidays.")

    if request.method == 'POST':
        name = request.POST.get('name')
        h_date = request.POST.get('holiday_date')
        h_type = request.POST.get('type')
        description = request.POST.get('description')

        if not name or not h_date:
            messages.error(request, "Name and Date are required.")
            return redirect('add_holiday')

        if Holiday.objects.filter(holiday_date=h_date).exists():
            messages.error(request, f"A holiday already exists on {h_date}.")
            return redirect('add_holiday')

        Holiday.objects.create(
            name=name,
            holiday_date=h_date,
            type=h_type,
            description=description
        )
        messages.success(request, 'Holiday added successfully!')
        return redirect('holiday_list')

    return render(request, 'academic/add-holiday.html')

@login_required
def delete_holiday(request, holiday_id):
    if not request.user.is_admin:
        return HttpResponseForbidden()
    
    holiday = get_object_or_404(Holiday, id=holiday_id)
    holiday.delete()
    messages.success(request, "Holiday deleted successfully!")
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