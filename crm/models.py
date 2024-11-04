from django.db import models
from django.contrib.auth.models import AbstractUser,User
import datetime
from django.db.models import Sum

class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.first_name} --> {self.last_name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150,null=True,blank=True)
    adress = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.first_name} --> {self.last_name}"


class Group(models.Model):
    name = models.CharField(max_length=150)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now=True,null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='teacher')

    def __str__(self) -> str:
        return f"{self.name}"
    
class Student(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    phone_number2 = models.CharField(max_length=150,null=True,blank=True)
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='stundet')
    group2 = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='student2',null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.first_name} --> {self.last_name}"
    
class Day(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='days',null=True,blank=True)
    date = models.DateField(default=datetime.date.today)  
    
    def __str__(self):
        return f"{self.date.strftime('%B %d, %Y')} - {self.group.name}"  
    
    @property
    def month(self):
        return self.date.strftime('%B') 

    @property
    def day_of_month(self):
        return self.date.day  

class Attendance(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='attendance',null=True,blank=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date = models.ForeignKey(Day,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

class Month(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='month')
    month = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.month} "

class Monthlypayment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tolovs')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tolov_sets')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="tolov_set")
    oylik = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.student.user.first_name} --> {self.student.user.last_name} ({self.oylik})"

    @classmethod
    def total_oylik_for_month(cls, month_id):
        return cls.objects.filter(month_id=month_id).aggregate(total_oylik=Sum('oylik'))['total_oylik'] or 0

