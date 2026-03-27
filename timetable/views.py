import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.core import serializers
from .models import TimeTable
from academic.models import Subject
from staff.models import Teacher
from django.conf import settings

def timetable_list(request):
    slots = TimeTable.objects.all().order_by('start_time')
    
    # Organisation par jour pour faciliter l'affichage dans le template
    schedule = {
        'Monday': slots.filter(day='Monday'),
        'Tuesday': slots.filter(day='Tuesday'),
        'Wednesday': slots.filter(day='Wednesday'),
        'Thursday': slots.filter(day='Thursday'),
        'Friday': slots.filter(day='Friday'),
        'Saturday': slots.filter(day='Saturday'),
    }
    
    return render(request, 'timetable/timetable.html', {'schedule': schedule})

def add_timetable(request):
    if not request.user.is_admin:
        return HttpResponseForbidden()

    if request.method == 'POST':
        day = request.POST.get('day')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        room = request.POST.get('classroom')

        TimeTable.objects.create(
            day=day,
            subject_id=subject_id,
            teacher_id=teacher_id,
            start_time=start,
            end_time=end,
            classroom=room
        )
        return redirect('timetable_list')

    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'timetable/add-timetable.html', {
        'subjects': subjects, 
        'teachers': teachers
    })



def visual_timetabling_embed(request):
    enabled = getattr(settings, 'VISUAL_TIMETABLING_ENABLED', True)
    external_url = getattr(settings, 'VISUAL_TIMETABLING_URL', 'https://www.visual-timetabling.be/')
    ctx = {
        'external_url': external_url if enabled else None,
        'integration_enabled': enabled,
    }
    return render(request, 'timetable/visual_tool.html', ctx)

def export_timetable_json(request):
    """Exporte les données au format JSON pour l'outil externe (Bonus points)"""
    data = list(TimeTable.objects.values(
        'day', 'subject__name', 'teacher__user__last_name', 'start_time', 'end_time', 'classroom'
    ))
    return HttpResponse(json.dumps(data, default=str), content_type="application/json")
