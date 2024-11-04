
from django.urls import path
from .views import RegisterAPIView,LoginAPIView,UserViewSet, TeacherViewSet, GroupViewSet, StudentViewSet,MonthlypaymentViewSet,MonthViewSet,AttendanceViewSet,DayViewSet




urlpatterns = [
    path('monthly-payment/', MonthlypaymentViewSet.as_view({'get': 'list','post':'create'})),
    path('monthly-payments/<int:pk>/', MonthlypaymentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('attdence/', AttendanceViewSet.as_view({'get': 'list','post':'create'})),
    path('attdence/<int:pk>/', AttendanceViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('days/', DayViewSet.as_view({'get': 'list','post':'create'})),
    path('day/<int:pk>/', DayViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('month/', MonthViewSet.as_view({'get': 'list','post':'create'})),
    path('month/<int:pk>/', MonthViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('group/', GroupViewSet.as_view({'get': 'list','post':'create'})),
    path('group/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('student/', StudentViewSet.as_view({'get': 'list','post':'create'})),
    path('student/<int:pk>/', StudentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('teacher/', TeacherViewSet.as_view({'get': 'list','post':'create'})),
    path('teacher/<int:pk>/', TeacherViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put':'put'})),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
