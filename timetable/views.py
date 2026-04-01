from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TimeTable, TimetableProposal
from academic.models import Subject, Department, Class
from staff.models import Teacher
from django.conf import settings


@login_required
def timetable_list(request):

    if request.user.is_admin:
        slots = TimeTable.objects.all()

    elif request.user.is_teacher:
        slots = TimeTable.objects.filter(
            teacher__user=request.user
        )

    elif hasattr(request.user, 'student'):
        student = request.user.student

        slots = TimeTable.objects.filter(
            student_class=student.student_class,
            
        )

    else:
        slots = TimeTable.objects.none()

    slots = slots.order_by('day', 'start_time')

    schedule = {
        'Monday': slots.filter(day='Monday'),
        'Tuesday': slots.filter(day='Tuesday'),
        'Wednesday': slots.filter(day='Wednesday'),
        'Thursday': slots.filter(day='Thursday'),
        'Friday': slots.filter(day='Friday'),
        'Saturday': slots.filter(day='Saturday'),
    }

    return render(request, 'timetable/timetable.html', {'schedule': schedule})


@login_required
def add_timetable(request):

    if not request.user.is_admin:
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        TimeTable.objects.create(
            day=request.POST.get('day'),
            subject_id=request.POST.get('subject'),
            teacher_id=request.POST.get('teacher'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            classroom=request.POST.get('classroom'),
            student_class_id=request.POST.get('student_class'),
            section=request.POST.get('section'),
        )
        return redirect('timetable_list')

    departments = Department.objects.all()

    return render(request, 'timetable/add-timetable.html', {
        'departments': departments,
    })


@login_required
def export_timetable_json(request):
    data = list(TimeTable.objects.values(
        'day',
        'subject__name',
        'teacher__user__last_name',
        'start_time',
        'end_time',
        'classroom'
    ))
    return JsonResponse(data, safe=False)


@login_required
def visual_timetabling_embed(request):
    enabled = getattr(settings, 'VISUAL_TIMETABLING_ENABLED', True)
    external_url = getattr(settings, 'VISUAL_TIMETABLING_URL', 'https://www.visual-timetabling.be/')

    return render(request, 'timetable/visual_tool.html', {
        'external_url': external_url if enabled else None,
        'integration_enabled': enabled,
    })


@login_required
def add_proposal(request):

    if not request.user.is_teacher:
        return HttpResponseForbidden("Access Denied")

    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        return HttpResponseForbidden("Teacher profile not found")

    subjects = Subject.objects.filter(teacher=teacher)
    classes = Class.objects.all()

    if request.method == 'POST':
        TimetableProposal.objects.create(
            teacher=teacher,
            subject_id=request.POST.get('subject'),
            student_class_id=request.POST.get('student_class'),  
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            classroom=request.POST.get('classroom'),
        )
        return redirect('proposal_list')

    return render(request, 'timetable/add_proposal.html', {
        'subjects': subjects,
        'classes': classes
    })

@login_required
def proposal_list(request):
    dept_id = request.GET.get('department')
    
    if request.user.is_admin:
        proposals = TimetableProposal.objects.all().select_related('subject', 'subject__department', 'teacher')
    elif request.user.is_teacher:
        teacher = Teacher.objects.filter(user=request.user).first()
        proposals = TimetableProposal.objects.filter(teacher=teacher).select_related('subject', 'subject__department', 'teacher')
    else:
        return HttpResponseForbidden("Access Denied")

    if dept_id:
        proposals = proposals.filter(subject__department_id=dept_id)

    departments = Department.objects.all()

    return render(request, 'timetable/proposal_list.html', {
        'proposals': proposals,
        'departments': departments,
        'selected_dept': dept_id
    })


@login_required
def approve_proposal(request, proposal_id):

    if not request.user.is_admin:
        return HttpResponseForbidden("Access Denied")

    proposal = get_object_or_404(TimetableProposal, id=proposal_id)

    proposal.status = 'Approved'
    proposal.save()

    TimeTable.objects.create(
        day=proposal.day,
        subject=proposal.subject,
        teacher=proposal.teacher,
        start_time=proposal.start_time,
        end_time=proposal.end_time,
        classroom=proposal.classroom,
        student_class=proposal.student_class,
    )

    return redirect('proposal_list')


@login_required
def reject_proposal(request, proposal_id):

    if not request.user.is_admin:
        return HttpResponseForbidden("Access Denied")

    proposal = get_object_or_404(TimetableProposal, id=proposal_id)

    if request.method == 'POST':
        proposal.status = 'Rejected'
        proposal.rejection_reason = request.POST.get('reason')
        proposal.save()

        return redirect('proposal_list')

    return render(request, 'timetable/reject_proposal.html', {
        'proposal': proposal
    })
def get_department_data(request, dept_id):
    subjects = Subject.objects.filter(department_id=dept_id)
    teachers = Teacher.objects.filter(department_id=dept_id)
    classes = Class.objects.filter(department_id=dept_id)

    data = {
        "subjects": [{"id": s.id, "name": s.name} for s in subjects],
        "teachers": [{"id": t.id, "name": str(t)} for t in teachers],
        "classes": [{"id": c.id, "name": c.name, "section": c.section} for c in classes],
    }

    return JsonResponse(data)