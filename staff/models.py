from django.db import models
from django.conf import settings 


class Teacher(models.Model):
    # Link to user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
   
    # Teacher info 
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        null=True,
        blank=True
    )

    qualification = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    experience = models.IntegerField(
        null=True,
        blank=True
    )

    mobile_number = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

    address = models.TextField(
        null=True,
        blank=True
    )

    joining_date = models.DateField(
        null=True,
        blank=True
    )

    # Department 
    department = models.ForeignKey(
        'academic.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"