from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Exam, Class, Student

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'user_type': 'student'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='testpassword', user_type='student')
        student = Student.objects.create(user=user, group='A', year_of_study=1)
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['id'], user.id)
        self.assertEqual(response.data['user']['student_id'], student.id)

class ExamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='studentuser', password='testpassword', user_type='student')
        self.client.force_authenticate(user=self.user)
        self.class_assigned = Class.objects.create(name='Test Class')
        self.class_assigned.students.add(Student.objects.create(user=self.user, group='A', year_of_study=1))
        self.create_exam_url = reverse('create-exam')

    def test_create_exam(self):
        data = {
            'subject': 'Math',
            'date': '2023-12-01T10:00:00Z',
            'location': 'Room 101',
            'class_assigned': self.class_assigned.id
        }
        response = self.client.post(self.create_exam_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exam.objects.count(), 1)
        self.assertEqual(Exam.objects.get().subject, 'Math')