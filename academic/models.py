from django.db import models
from django.conf import settings
from staff.models import Teacher


class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_dept = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name="managed_department"
    )

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.department.name} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)

    date = models.DateField()
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    mark = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.mark}"


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    holiday_date = models.DateField()
    type = models.CharField(
        max_length=50,
        choices=[('Public', 'Public'), ('School', 'School')]
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SubjectProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    proposer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    marks = models.FloatField(null=True, blank=True)