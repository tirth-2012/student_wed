from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('', views.index,name='index'),
    path('index/', views.index,name='index'),
    path('addstudent/', views.addstudent,name='addstudent'),
    path('studentlist/', views.studentlist,name='studentlist'),
    path('course-report/', views.course_report, name='course_report'),
    path('report/', views.report_view, name='student_report'),
    path('report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('fees/', views.fees, name='fees'),
    path('feeslist/', views.fees_list, name='fees_list'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
]
