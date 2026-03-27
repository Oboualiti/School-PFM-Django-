from django.db import models
from staff.models import Teacher
from student.models import Student

class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_dept = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="managed_department")

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=100) # Ex: Contrôle 1
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()

class Grade(models.Model): # Pour la saisie des résultats
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    mark = models.FloatField()

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    holiday_date = models.DateField()
    type = models.CharField(max_length=50, choices=[('Public', 'Public'), ('School', 'School')])

    def __str__(self):
        return self.name