from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, PasswordResetRequest
from staff.models import Teacher  


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        role = request.POST.get('role')

        # Password check
        if not password or password != confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/register.html')

        # Email check
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'authentication/register.html')

        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        # Reset roles
        user.is_student = False
        user.is_teacher = False
        user.is_admin = False
        user.is_staff = False

        # Assign ONE role only
        if role == 'student':
            user.is_student = True

        elif role == 'teacher':
            user.is_teacher = True

        # DO NOT allow admin from signup

        user.save()

        # CREATE TEACHER PROFILE 
        if user.is_teacher:
            Teacher.objects.get_or_create(user=user)

        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('index')

    return render(request, 'authentication/register.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email)
            reset_request.send_reset_email()
            messages.success(request, 'A reset link has been sent to your email.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No user found with this email.')
        
        return redirect('login')
    
    return render(request, 'authentication/forgot-password.html')


def reset_password_view(request, token):
    reset_request = get_object_or_404(PasswordResetRequest, token=token)
    
    if not reset_request.is_valid():
        messages.error(request, 'This reset link has expired.')
        return redirect('forgot-password')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user = reset_request.user
            user.set_password(new_password)
            user.save()
            reset_request.delete()
            messages.success(request, 'Password reset successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            
    return render(request, 'authentication/reset_password.html', {'token': token})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            if user.is_admin or user.is_teacher:
                return redirect('dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')