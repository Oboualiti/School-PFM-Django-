from django.db import models
from academic.models import Subject, Class
from staff.models import Teacher


class TimeTable(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day = models.CharField(max_length=20, choices=DAYS)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    start_time = models.TimeField()
    end_time = models.TimeField()

    classroom = models.CharField(max_length=50)

    student_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    section = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.day} - {self.subject.name} ({self.classroom})"


class TimetableProposal(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    student_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    day = models.CharField(max_length=15)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.CharField(max_length=50)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.teacher} - {self.subject} ({self.day})"