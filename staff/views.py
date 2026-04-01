from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home_auth.decorators import admin_required
from home_auth.models import CustomUser
from .models import Teacher
from academic.models import Department


@login_required
def teacher_list(request):
    dept_id = request.GET.get('department')
    teachers = Teacher.objects.all().select_related('user', 'department')
    
    if dept_id:
        teachers = teachers.filter(department_id=dept_id)
        
    departments = Department.objects.all()
    
    return render(request, 'staff/teacher-list.html', {
        'teachers': teachers,
        'departments': departments,
        'selected_dept': dept_id
    })


@admin_required
def add_teacher(request):
    """Add a new teacher"""
    if request.method == 'POST':
        # Get user data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Get teacher data
        gender = request.POST.get('gender')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        joining_date = request.POST.get('joining_date')
        department_id = request.POST.get('department')
        
        try:
            # Create user account
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_teacher=True
            )
            
            # Get department
            department = None
            if department_id:
                department = Department.objects.get(id=department_id)
            
            # Create teacher profile
            Teacher.objects.create(
                user=user,
                gender=gender,
                qualification=qualification,
                experience=int(experience) if experience else 0,
                mobile_number=mobile_number,
                address=address,
                joining_date=joining_date or None,
                department=department
            )
            
            messages.success(request, 'Teacher added successfully')
            return redirect('teacher_list')
        except Exception as e:
            messages.error(request, f'Error creating teacher: {str(e)}')
    
    departments = Department.objects.all()
    return render(request, 'staff/add-teacher.html', {'departments': departments})


@admin_required
def edit_teacher(request, teacher_id):
    """Edit teacher details"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        # Update user data
        teacher.user.first_name = request.POST.get('first_name')
        teacher.user.last_name = request.POST.get('last_name')
        teacher.user.email = request.POST.get('email')
        teacher.user.save()
        
        # Update teacher data
        teacher.gender = request.POST.get('gender')
        teacher.qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        teacher.experience = int(experience) if experience else 0
        teacher.mobile_number = request.POST.get('mobile_number')
        teacher.address = request.POST.get('address')
        teacher.joining_date = request.POST.get('joining_date') or None
        
        department_id = request.POST.get('department')
        if department_id:
            teacher.department = Department.objects.get(id=department_id)
        
        teacher.save()
        messages.success(request, 'Teacher updated successfully')
        return redirect('teacher_list')
    
    departments = Department.objects.all()
    return render(request, 'staff/edit-teacher.html', {
        'teacher': teacher,
        'departments': departments
    })


@admin_required
def delete_teacher(request, teacher_id):
    """Delete a teacher"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user_id = teacher.user.id
    
    teacher.delete()
    CustomUser.objects.filter(id=user_id).delete()
    
    messages.success(request, 'Teacher deleted successfully')
    return redirect('teacher_list')

