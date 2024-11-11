from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom user model manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, hash_code, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not hash_code:
            raise ValueError('The Hash code field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, hash_code=hash_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, hash_code, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, hash_code, password, **extra_fields)

# Custom user model
class CustomUser(AbstractBaseUser):
    ROLES = [
        ('STUDENT', 'Student'),
        ('PROFESSOR', 'Professor'),
        ('ADMIN', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    hash_code = models.CharField(max_length=64, unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='STUDENT')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['hash_code']

    def __str__(self):
        return self.email

# Model for Class (for Students)
class Class(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(CustomUser, limit_choices_to={'role': 'STUDENT'})

    def __str__(self):
        return self.name

# Model for Subject
class Subject(models.Model):
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class, related_name='subjects')
    professors = models.ManyToManyField(CustomUser, limit_choices_to={'role': 'PROFESSOR'})

    def __str__(self):
        return self.name

# Model for Exam
class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    rooms = models.CharField(max_length=200)  # Example: "Amf. RR, C207"
    allowed_classes = models.ManyToManyField(Class)
    
    def __str__(self):
        return f"{self.subject.name} Exam on {self.start_time}"
