from rest_framework import serializers
from .models import Teacher,Month,Monthlypayment,Student,Day,Attendance,Group
from .models import User
from django.contrib.auth import get_user_model

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)



User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User  
        fields = ('username', 'password', 'first_name', 'last_name')  

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
