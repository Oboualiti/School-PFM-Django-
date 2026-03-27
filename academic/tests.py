from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from academic.models import Department, Subject, Exam, Holiday
from staff.models import Teacher

User = get_user_model()

class AcademicViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u@example.com', email='u@example.com', password='pass')
        self.user.is_admin = True
        self.user.save()
        self.client.force_login(self.user)
        self.teacher_user = User.objects.create_user(username='t@example.com', email='t@example.com', password='pass')
        self.teacher = Teacher.objects.create(user=self.teacher_user, gender='Male', qualification='Q', experience=1, mobile_number='1', address='A', joining_date='2026-01-01', department=None)
        self.dept = Department.objects.create(name='Science', head_of_dept=None)
        self.subject = Subject.objects.create(name='Math', department=self.dept, teacher=self.teacher)
        self.exam = Exam.objects.create(name='Mid', subject=self.subject, date='2026-01-10')
        self.holiday = Holiday.objects.create(name='X', holiday_date='2026-01-15', type='Public')

    def test_subject_list(self):
        resp = self.client.get(reverse('subject_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Subjects')

    def test_exam_list(self):
        resp = self.client.get(reverse('exam_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Exams')

    def test_holiday_list(self):
        resp = self.client.get(reverse('holiday_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Holidays')
