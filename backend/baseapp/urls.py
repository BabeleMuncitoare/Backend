from django.urls import path
from .views import (
    RegisterView, LoginView, ExamListView, StudentExamListView, ProfessorExamListView, 
    ProfessorListView, CreateExamView, AcceptExamView, CreateClassView, ClassListView, 
    ClassDetailView, ExamDetailView, PendingExamsListView, StudentExamsListView, 
    RejectExamView, AdminUserManagementView, AdminUserDetailView, AdminClassManagementView, 
    AdminClassDetailView, AdminExamManagementView, AdminExamDetailView, 
    AdminProfessorManagementView, AdminProfessorDetailView,
    AnnouncementListView, AdminAnnouncementManagementView, AdminAnnouncementDetailView 
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('exams/', ExamListView.as_view(), name='exam-list'),
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('student/exams/', StudentExamListView.as_view(), name='student-exams'),
    path('professor/exams/', ProfessorExamListView.as_view(), name='professor-exams'),
    path('professors/', ProfessorListView.as_view(), name='professor-list'),
    path('exams/create/', CreateExamView.as_view(), name='create-exam'),
    path('exams/<int:pk>/accept/', AcceptExamView.as_view(), name='accept-exam'),
    path('exams/<int:pk>/reject/', RejectExamView.as_view(), name='reject-exam'),
    path('classes/create/', CreateClassView.as_view(), name='create-class'),
    path('classes/', ClassListView.as_view(), name='class-list'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),
    path('professor/pending-exams/', PendingExamsListView.as_view(), name='pending-exams'),
    path('student/exams/', StudentExamsListView.as_view(), name='student-exams'),
    path('admin/users/', AdminUserManagementView.as_view(), name='admin-user-management'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/classes/', AdminClassManagementView.as_view(), name='admin-class-management'),
    path('admin/classes/<int:pk>/', AdminClassDetailView.as_view(), name='admin-class-detail'),
    path('admin/exams/', AdminExamManagementView.as_view(), name='admin-exam-management'),
    path('admin/exams/<int:pk>/', AdminExamDetailView.as_view(), name='admin-exam-detail'),
    path('admin/professors/', AdminProfessorManagementView.as_view(), name='admin-professor-management'),
    path('admin/professors/<int:pk>/', AdminProfessorDetailView.as_view(), name='admin-professor-detail'),
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
    path('admin/announcements/', AdminAnnouncementManagementView.as_view(), name='admin-announcement-management'),
    path('admin/announcements/<int:pk>/', AdminAnnouncementDetailView.as_view(), name='admin-announcement-detail'),
]