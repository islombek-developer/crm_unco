
from django.urls import path
from .views import TeacherAPIView,RegisterAPIView,LoginAPIView


urlpatterns = [
    path('teacher/', TeacherAPIView.as_view({'get': 'list','post':'create'})),
    path('teacher/<int:pk>/', TeacherAPIView.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
