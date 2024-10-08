from django.contrib import admin
from .models import Teacher,Admin,Month,Monthlypayment,Student,Day,Attendance,Group

admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Month)
admin.site.register(Monthlypayment)
admin.site.register(Student)
admin.site.register(Day)
admin.site.register(Group)
admin.site.register(Attendance)