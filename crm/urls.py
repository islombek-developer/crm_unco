
from django.urls import path
from .views import RegisterAPIView,LoginAPIView,UserViewSet, TeacherViewSet, GroupViewSet, StudentViewSet


urlpatterns = [
    path('group/', GroupViewSet.as_view({'get': 'list','post':'create'})),
    path('group/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('student/', StudentViewSet.as_view({'get': 'list','post':'create'})),
    path('student/<int:pk>/', StudentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('teacher/', TeacherViewSet.as_view({'get': 'list','post':'create'})),
    path('teacher/<int:pk>/', TeacherViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put':'put'})),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
