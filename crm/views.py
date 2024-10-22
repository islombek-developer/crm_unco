from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Teacher,User,Month,Monthlypayment,Student,Day,Attendance,Group
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import TeacherSerializer,RegisterSerializer, LoginSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

class TeacherPagination(PageNumberPagination):
    page_size = 3
        
class TeacherAPIView(viewsets.ModelViewSet):
    pagination_classes = TeacherPagination
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()



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