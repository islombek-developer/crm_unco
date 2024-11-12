from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path,include
from .views import RegisterAPIView,LoginAPIView,UserViewSet, TeacherViewSet, GroupViewSet, StudentViewSet,MonthlypaymentViewSet,MonthViewSet,AttendanceViewSet,DayViewSet
from django.conf import settings



urlpatterns = [
    path('monthly-payment/', MonthlypaymentViewSet.as_view({'get': 'list','post':'create'})),
    path('monthly-payment/<int:pk>/', MonthlypaymentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put': 'update'})),
    path('attdence/', AttendanceViewSet.as_view({'get': 'list','post':'create'})),
    path('attdence/<int:pk>/', AttendanceViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put': 'update'})),
    path('day/', DayViewSet.as_view({'get': 'list','post':'create'})),
    path('day/<int:pk>/', DayViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put': 'update'})),
    path('month/', MonthViewSet.as_view({'get': 'list','post':'create'})),
    path('month/<int:pk>/', MonthViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('group/', GroupViewSet.as_view({'get': 'list','post':'create'})),
    path('group/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put': 'update'})),
    path('student/', StudentViewSet.as_view({'get': 'list','post':'create'})),
    path('student/<int:pk>/', StudentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put': 'update'})),
    path('teacher/', TeacherViewSet.as_view({'get': 'list','post':'create'})),
    path('teacher/<int:pk>/', TeacherViewSet.as_view({'get': 'retrieve', 'delete': 'destroy','put': 'update'})),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]