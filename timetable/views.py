from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from .models import TimeTable, TimetableProposal
from academic.models import Subject
from staff.models import Teacher
from django.conf import settings


# VIEW TIMETABLE
def timetable_list(request):

    if request.user.is_admin:
        slots = TimeTable.objects.all()

    elif hasattr(request.user, 'teacher_profile'):
        slots = TimeTable.objects.filter(
            teacher=request.user.teacher_profile
        )

    elif hasattr(request.user, 'student'):
        student = request.user.student
        slots = TimeTable.objects.filter(
            student_class=student.student_class,
            section=student.section
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

# ADMIN ADD TIMETABLE
def add_timetable(request):

    if not request.user.is_admin:
        return HttpResponseForbidden()

    if request.method == 'POST':
        TimeTable.objects.create(
            day=request.POST.get('day'),
            subject_id=request.POST.get('subject'),
            teacher_id=request.POST.get('teacher'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            classroom=request.POST.get('classroom')
        )
        return redirect('timetable_list')

    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    return render(request, 'timetable/add-timetable.html', {
        'subjects': subjects,
        'teachers': teachers
    })


# EXPORT JSON
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


# VISUAL TOOL
def visual_timetabling_embed(request):
    enabled = getattr(settings, 'VISUAL_TIMETABLING_ENABLED', True)
    external_url = getattr(settings, 'VISUAL_TIMETABLING_URL', 'https://www.visual-timetabling.be/')

    return render(request, 'timetable/visual_tool.html', {
        'external_url': external_url if enabled else None,
        'integration_enabled': enabled,
    })


# ADD PROPOSAL
def add_proposal(request):

    if not hasattr(request.user, 'teacher_profile'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        TimetableProposal.objects.create(
            teacher=request.user.teacher_profile,
            subject_id=request.POST.get('subject'),
            day=request.POST.get('day'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            classroom=request.POST.get('classroom'),
        )
        return redirect('proposal_list')

    subjects = Subject.objects.all()

    return render(request, 'timetable/add_proposal.html', {
        'subjects': subjects
    })



# LIST PROPOSALS

def proposal_list(request):
    print("USER:", request.user)

    if request.user.is_admin:
        proposals = TimetableProposal.objects.all()

    elif hasattr(request.user, 'teacher_profile'):
        proposals = TimetableProposal.objects.filter(
            teacher=request.user.teacher_profile
        )

    else:
        return HttpResponseForbidden()

    print("PROPOSALS:", proposals)

    return render(request, 'timetable/proposal_list.html', {
        'proposals': proposals
    })

# APPROVE PROPOSAL (ADMIN)
def approve_proposal(request, proposal_id):
    if not request.user.is_admin:
        return HttpResponseForbidden()

    proposal = get_object_or_404(TimetableProposal, id=proposal_id)

    proposal.status = 'Approved'
    proposal.rejection_reason = ''  # clear any old reason
    proposal.save()

    # create timetable
    TimeTable.objects.create(
        day=proposal.day,
        subject=proposal.subject,
        teacher=proposal.teacher,
        start_time=proposal.start_time,
        end_time=proposal.end_time,
        classroom=proposal.classroom,
    )

    return redirect('proposal_list')

    # create timetable
    TimeTable.objects.create(
        day=proposal.day,
        subject=proposal.subject,
        teacher=proposal.teacher,
        start_time=proposal.start_time,
        end_time=proposal.end_time,
        classroom=proposal.classroom
    )

    return redirect('proposal_list')

def reject_proposal(request, proposal_id):
    if not request.user.is_admin:
        return HttpResponseForbidden()

    proposal = get_object_or_404(TimetableProposal, id=proposal_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')

        proposal.status = 'Rejected'
        proposal.rejection_reason = reason
        proposal.save()

        return redirect('proposal_list')

    return render(request, 'timetable/reject_proposal.html', {
        'proposal': proposal
    })