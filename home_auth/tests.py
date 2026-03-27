from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupFlowTest(TestCase):
    def test_signup_creates_student_and_logs_in(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'pass1234',
            'confirm_password': 'pass1234',
        }
        resp = self.client.post(reverse('signup'), data, follow=True)
        self.assertEqual(resp.status_code, 200)
        u = User.objects.get(email='john@example.com')
        self.assertTrue(u.is_student)
        self.assertTrue(u.is_active)
