# filepath: /c:/Users/Yirade/ip proj/backend/baseapp/serializers.py
from rest_framework import serializers
from .models import User, Student, Professor, Exam, Class, Announcement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        if validated_data['user_type'] == 'professor':
            Professor.objects.create(user=user, department='Unknown')
        elif validated_data['user_type'] == 'student':
            Student.objects.create(user=user, group='Unknown', year_of_study=1)
        return user

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['created_by', 'accepted', 'rejected']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ProfessorSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Professor
        fields = ['id', 'user', 'user_name', 'department']

class StudentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'user_name', 'group', 'year_of_study']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']