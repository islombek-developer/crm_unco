from rest_framework import serializers
from .models import Teacher,Month,Monthlypayment,Student,Day,Attendance
from .models import User,Group
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'phone_number', 'address']
        read_only_fields = ['id']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'adress']
        read_only_fields = ['id']

class GroupSerializer(serializers.ModelSerializer):
    # teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        write_only=True,
        source='teacher'
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'start_date', 'end_date',  'teacher_id']
        read_only_fields = ['id', 'start_date', 'end_date']

class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        source='group'
    )
    group2 = GroupSerializer(read_only=True)
    group2_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        source='group2',
        required=False
    )

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'phone_number2', 
                 'group', 'group_id', 'group2', 'group2_id']
        read_only_fields = ['id']


class DaySerializer(serializers.ModelSerializer):
    month = serializers.ReadOnlyField()
    day_of_month = serializers.ReadOnlyField()
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        source='group'
    )

    class Meta:
        model = Day
        fields = ['id', 'date', 'group', 'group_id', 'month', 'day_of_month']
        read_only_fields = ['id']

class AttendanceSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        source='group'
    )
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        write_only=True,
        source='student'
    )
    date = DaySerializer(read_only=True)
    date_id = serializers.PrimaryKeyRelatedField(
        queryset=Day.objects.all(),
        write_only=True,
        source='date'
    )

    class Meta:
        model = Attendance
        fields = ['id', 'group', 'group_id', 'student', 'student_id', 
                 'date', 'date_id', 'status']
        read_only_fields = ['id']

class MonthSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        source='group'
    )

    class Meta:
        model = Month
        fields = ['id', 'group', 'group_id', 'month']
        read_only_fields = ['id']

class MonthlypaymentSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        source='group'
    )
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        write_only=True,
        source='student'
    )
    month = MonthSerializer(read_only=True)
    month_id = serializers.PrimaryKeyRelatedField(
        queryset=Month.objects.all(),
        write_only=True,
        source='month'
    )
    total_oylik = serializers.SerializerMethodField()

    class Meta:
        model = Monthlypayment
        fields = ['id', 'group', 'group_id', 'student', 'student_id', 
                 'month', 'month_id', 'oylik', 'total_oylik']
        read_only_fields = ['id', 'total_oylik']

    def get_total_oylik(self, obj):
        return Monthlypayment.total_oylik_for_month(obj.month.id)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)



User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User  
        fields = ('username', 'password', 'first_name','image', 'last_name')  

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
