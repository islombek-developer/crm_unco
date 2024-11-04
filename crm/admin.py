from django.contrib import admin
from .models import Teacher,User,Month,Monthlypayment,Student,Day,Attendance,Group


admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Month)
admin.site.register(Monthlypayment)
admin.site.register(Student)
admin.site.register(Day)
admin.site.register(Group)
admin.site.register(Attendance)