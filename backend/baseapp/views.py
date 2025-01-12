from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Exam, Student, Professor, Class, User, Announcement
from .serializers import UserSerializer, ExamSerializer, LoginSerializer, ProfessorSerializer, ClassSerializer, AnnouncementSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                }
            })

        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentExamListView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return Exam.objects.filter(class_assigned__students=student)

class ProfessorExamListView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        professor = Professor.objects.get(user=self.request.user)
        return Exam.objects.filter(class_assigned__professor=professor)

class ProfessorListView(generics.ListAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateExamView(generics.CreateAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            student = Student.objects.get(user=self.request.user)
            serializer.save(created_by=student)
        except Student.DoesNotExist:
            raise ValidationError("You must be a student to create an exam.")

class AcceptExamView(generics.UpdateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        exam = self.get_object()
        professor = Professor.objects.get(user=self.request.user)
        if professor in exam.class_assigned.professors.all():
            exam.accepted = True
            exam.rejected = False
            exam.save()
            return Response({'status': 'Exam accepted'})
        return Response({'error': 'You are not authorized to accept this exam'}, status=status.HTTP_403_FORBIDDEN)

class CreateClassView(generics.CreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class ClassListView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            student = Student.objects.get(user=user)
            return Class.objects.filter(students=student)
        return Class.objects.none()

class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class PendingExamsListView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        professor = Professor.objects.get(user=self.request.user)
        return Exam.objects.filter(class_assigned__professors=professor, accepted=False)
    
class StudentExamsListView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            student = Student.objects.get(user=user)
            return Exam.objects.filter(class_assigned__students=student)
        elif user.user_type == 'professor':
            professor = Professor.objects.get(user=user)
            return Exam.objects.filter(class_assigned__professors=professor)
        else:
            return Exam.objects.none()
        
class RejectExamView(generics.UpdateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        exam = self.get_object()
        professor = Professor.objects.get(user=self.request.user)
        if professor in exam.class_assigned.professors.all():
            exam.rejected = True
            exam.accepted = False
            exam.save()
            return Response({'status': 'Exam rejected'})
        return Response({'error': 'You are not authorized to reject this exam'}, status=status.HTTP_403_FORBIDDEN)
    


# Custom permission to restrict access to admins only
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'

# Admin: List, Create, Update, and Delete Users
class AdminUserManagementView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Admin: List, Create, Update, and Delete Classes
class AdminClassManagementView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminUser]

class AdminClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminUser]

# Admin: List, Create, Update, and Delete Exams
class AdminExamManagementView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminUser]

class AdminExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminUser]

# Admin: List, Create, Update, and Delete Professors
class AdminProfessorManagementView(generics.ListCreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAdminUser]

class AdminProfessorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAdminUser]

class AnnouncementListView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = []  # Publicly accessible

class AdminAnnouncementManagementView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminUser]

class AdminAnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminUser]
