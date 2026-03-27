from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'gender', 'qualification', 'experience', 'mobile_number', 'joining_date')
    list_filter = ('gender', 'qualification', 'joining_date')
    search_fields = ('user__first_name', 'user__last_name', 'mobile_number')
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'
