from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Student, Parent

User = get_user_model()

class StudentRBAC(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='a@example.com', email='a@example.com', password='pass', is_admin=True)
        self.student_user = User.objects.create_user(username='s@example.com', email='s@example.com', password='pass', is_student=True)
        parent = Parent.objects.create(
            father_name='F', father_occupation='', father_mobile='1', father_email='f@example.com',
            mother_name='M', mother_occupation='', mother_mobile='2', mother_email='m@example.com',
            present_address='A', permanent_address='B'
        )
        self.student = Student.objects.create(
            parent=parent, user=self.student_user, first_name='Stu', last_name='Dent', student_id='S1',
            gender='Male', date_of_birth='2026-01-01', student_class='C', joining_date='2026-01-02',
            mobile_number='123', admission_number='ADM', section='SEC'
        )
        parent2 = Parent.objects.create(
            father_name='F2', father_occupation='', father_mobile='3', father_email='f2@example.com',
            mother_name='M2', mother_occupation='', mother_mobile='4', mother_email='m2@example.com',
            present_address='A2', permanent_address='B2'
        )
        self.other = Student.objects.create(
            parent=parent2, user=None, first_name='Other', last_name='User', student_id='S2',
            gender='Male', date_of_birth='2026-01-01', student_class='C', joining_date='2026-01-02',
            mobile_number='456', admission_number='ADM2', section='SEC'
        )

    def test_student_list_visible(self):
        self.client.force_login(self.student_user)
        resp = self.client.get(reverse('student_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Students')
        self.assertNotContains(resp, 'fas fa-plus')  # no add button for student

    def test_student_cannot_add_delete(self):
        self.client.force_login(self.student_user)
        resp = self.client.get(reverse('add_student'))
        self.assertEqual(resp.status_code, 302)  # redirected by admin_required
        resp = self.client.post(reverse('delete_student', args=[self.other.student_id]))
        self.assertIn(resp.status_code, (302, 403))

    def test_student_cannot_edit_others(self):
        self.client.force_login(self.student_user)
        resp = self.client.get(reverse('edit_student', args=[self.other.student_id]))
        self.assertEqual(resp.status_code, 403)

    def test_student_can_view_and_edit_self(self):
        self.client.force_login(self.student_user)
        resp = self.client.get(reverse('view_student', args=[self.student.student_id]))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('edit_student', args=[self.student.student_id]), {
            'first_name': 'Stu2',
            'last_name': 'Dent',
            'student_id': 'S1',
            'gender': 'Male',
            'date_of_birth': '2026-01-01',
            'student_class': 'C',
            'joining_date': '2026-01-02',
            'mobile_number': '123',
            'admission_number': 'ADM',
            'section': 'SEC',
            'father_name': 'F',
            'father_occupation': '',
            'father_mobile': '1',
            'father_email': 'f@example.com',
            'mother_name': 'M',
            'mother_occupation': '',
            'mother_mobile': '2',
            'mother_email': 'm@example.com',
            'present_address': 'A',
            'permanent_address': 'B'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
