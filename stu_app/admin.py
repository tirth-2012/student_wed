from django.contrib import admin
from .models import Student,Fees,Attendance

# Register your models here.

admin.site.register(Student)
admin.site.register(Fees)
admin.site.register(Attendance)
