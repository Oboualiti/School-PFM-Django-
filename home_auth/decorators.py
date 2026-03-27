from django.contrib.auth.decorators import user_passes_test

def admin_required(function):
    return user_passes_test(lambda u: u.is_authenticated and u.is_admin)(function)

def teacher_required(function):
    return user_passes_test(lambda u: u.is_authenticated and u.is_teacher)(function)