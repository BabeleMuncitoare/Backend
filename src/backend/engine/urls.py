from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ClassViewSet, SubjectViewSet, ExamViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'exams', ExamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
