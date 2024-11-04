from django.contrib.auth import authenticate
from .models import Teacher,User,Month,Monthlypayment,Student,Day,Attendance,Group
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer,UserSerializer, TeacherSerializer, GroupSerializer, StudentSerializer,DaySerializer,MonthlypaymentSerializer,AttendanceSerializer,MonthSerializer
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, filters,status,generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from datetime import datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ['first_name', 'last_name']

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ['first_name', 'last_name']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'teacher']
    search_fields = ['name', 'teacher__first_name', 'teacher__last_name']
    ordering_fields = ['name', 'start_date', 'end_date']

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name', 'group', 'group2']
    search_fields = ['first_name', 'last_name', 'phone_number', 'phone_number2']
    ordering_fields = ['first_name', 'last_name']



class DayViewSet(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'date']
    search_fields = ['group__name']
    ordering_fields = ['date']

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year', datetime.now().year)
        
        if month:
            days = self.queryset.filter(
                date__year=year,
                date__month=datetime.strptime(month, '%B').month
            )
            serializer = self.get_serializer(days, many=True)
            return Response(serializer.data)
        return Response({'error': 'Month parameter is required'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'student', 'date', 'status']
    search_fields = ['student__first_name', 'student__last_name']
    ordering_fields = ['date__date']

    @action(detail=False, methods=['get'])
    def student_attendance(self, request):
        student_id = request.query_params.get('student_id')
        month = request.query_params.get('month')
        
        if student_id and month:
            attendance = self.queryset.filter(
                student_id=student_id,
                date__date__month=datetime.strptime(month, '%B').month
            ).values('status').annotate(count=Count('status'))
            return Response(attendance)
        return Response({'error': 'Both student_id and month parameters are required'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class MonthViewSet(viewsets.ModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'month']
    search_fields = ['month', 'group__name']
    ordering_fields = ['month']

class MonthlypaymentViewSet(viewsets.ModelViewSet):
    queryset = Monthlypayment.objects.all()
    serializer_class = MonthlypaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'student', 'month']
    search_fields = ['student__first_name', 'student__last_name']
    ordering_fields = ['oylik']

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        month_id = request.query_params.get('month_id')
        group_id = request.query_params.get('group_id')
        
        if month_id and group_id:
            payments = self.queryset.filter(
                month_id=month_id,
                group_id=group_id
            ).aggregate(
                total_payments=Sum('oylik'),
                student_count=Count('student', distinct=True)
            )
            return Response(payments)
        return Response({'error': 'Both month_id and group_id parameters are required'}, 
                      status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "password": user.password,
            },
            "message": "Account created successfully."
        }, status=status.HTTP_201_CREATED)
    


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
