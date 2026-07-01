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
    path('logout_user',views.logout_user,name="logout_user"),
    path('login',views.login,name="login"),
    path('register',views.register,name="register"),
    path('api/generate-code', views.generate_volunteer_code, name='generate_code'),
    path('api/get-codes', views.get_volunteer_codes, name='get_codes'),
    path('api/deactivate-code', views.deactivate_code, name='deactivate_code'),
    path('volunteer-panel', views.volunteer_panel, name='volunteer_panel'),
    path('api/expenses-with-docs', views.get_expenses_with_documents, name='expenses_with_docs'),
    path('api/student-expense-summary/<int:student_id>', views.get_student_expense_summary, name='student_expense_summary'),
    path('api/student-expenses-detail/<int:student_id>', views.get_student_expenses_with_docs, name='student_expenses_with_docs'),
    path('api/expenses-summary', views.get_expenses_summary, name='expenses_summary'),
    path('api/download-document/<int:document_id>', views.download_expense_document, name='download_document'),
    path('report',views.report,name="report"),
    #path('insert',views.insert,name="insert")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])