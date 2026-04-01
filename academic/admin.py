from django.contrib import admin
from .models import Class, Department, Subject, Exam, Grade, Holiday, SubjectProposal
admin.site.register(Class)
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_dept')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'teacher')
    list_filter = ('department', 'teacher')
    search_fields = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date')
    list_filter = ('date', 'subject')
    search_fields = ('name',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'mark')
    list_filter = ('exam', 'mark')
    search_fields = ('student__first_name', 'student__last_name')

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'holiday_date', 'type')
    list_filter = ('type', 'holiday_date')
    search_fields = ('name',)

