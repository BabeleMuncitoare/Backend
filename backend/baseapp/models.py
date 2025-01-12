# baseapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=100)
    year_of_study = models.PositiveIntegerField()

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

class Class(models.Model):
    name = models.CharField(max_length=255)
    professors = models.ManyToManyField(Professor)
    students = models.ManyToManyField(Student)

class Exam(models.Model):
    subject = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title