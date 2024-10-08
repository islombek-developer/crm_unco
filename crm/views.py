from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Teacher,Admin,Month,Monthlypayment,Student,Day,Attendance,Group

