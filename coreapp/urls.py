from django.contrib import admin
from django.urls import path
from coreapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    #path('',views.index,name='home'),
    #path('about',views.about,name='about'),
    #path('register',views.register,name='register'),
    path('dashboard', views.dashboard_view, name='dashboard'), # Renders dashboard.html
    path('students-list', views.records_view, name='records_page'), # Renders student_list.html
    path('attendance',views.attendance_view,name="attendance"),#render the attendance.html
    # APIs
    path('api', views.dashboard, name='dashboard_api'), 
    path('api/students', views.get_student, name='get_student_api'),
    path('insert', views.insert_data, name='insert'),
    path('put_attendance', views.put_attendance, name='attendence'),
    path('getdetails',views.get_details_students,name="get_studentdetails"),
    path('delete_attendance',views.delete_attendence_api,name='delete_attendence'),
    path('get_attendance_exists',views.attendance_exixting,name="atttendance_exists"),
    path('check_attendance',views.check_attendance,name="check_attendance"),
    path('update_student/<int:student_id>',views.update_student_data,name="update_student_data"),
    path('expenses',views.expenses,name="expenses"),
    path('upload_expense/<int:expense_id>',views.upload_expense_receipt,name="upload_expenses"),
    path('register_user',views.register_user,name="register_user"),
    path('login_user',views.login_user,name="login_user"),
    path('login',views.login,name="login"),
    path('register',views.register,name="register"),
    
    #path('insert',views.insert,name="insert")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])