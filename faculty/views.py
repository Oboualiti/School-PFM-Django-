from django.shortcuts import render
from django.http import HttpResponse
from staff.models import Teacher


# Create your views here.

def index(request):
    return render(request, 'authentication/login.html')

def dashboard(request):
    return render(request, 'students/student-dashboard.html')

def ui_test(request):
    return render(request, 'tests/ui_smoke.html')


