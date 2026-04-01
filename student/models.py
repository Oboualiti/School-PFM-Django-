from django.db import models
from django.conf import settings


class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=15)
    father_email = models.EmailField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=15)
    mother_email = models.EmailField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self):
        return f"{self.father_name} & {self.mother_name}"


class Student(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    student_id = models.CharField(max_length=200, blank=True)

    student_class = models.ForeignKey('academic.Class', on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )

    date_of_birth = models.DateField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    admission_number = models.CharField(max_length=20, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)

    student_image = models.ImageField(upload_to='students/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Student.objects.exclude(student_id="").order_by('id').last()

            if last_student and last_student.student_id:
                last_id = int(last_student.student_id[3:])
                new_id = last_id + 1
            else:
                new_id = 1

            self.student_id = "STU" + str(new_id).zfill(4)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        if not full_name and self.user:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name if full_name else f"Student ({self.student_id})"