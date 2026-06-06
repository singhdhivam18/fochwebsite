from django.urls import path
from coreapp import views

urlpatterns = [

    # ========== PUBLIC ROUTES ==========
    path('login',    views.login,    name="login"),
    path('register', views.register, name="register"),

    # ========== AUTHENTICATED ROUTES (Any logged-in user) ==========
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('api',       views.get_dashboard,  name='dashboard_api'),   # renamed: was views.dashboard

    # ========== VOLUNTEER-ONLY: STUDENTS ==========
    path('students-list',                    views.records_view,       name='records_page'),
    path('api/students',                     views.get_student,        name='get_student_api'),
    path('insert',                           views.insert_data,        name='insert'),
    path('update_student/<int:student_id>',  views.update_student_data, name='update_student_data'),

    # ========== VOLUNTEER-ONLY: ATTENDANCE ==========
    path('attendance',           views.attendance_view,     name='attendance'),
    path('put_attendance',       views.put_attendance,      name='attendence'),
    path('getdetails',           views.get_details_students, name='get_studentdetails'),
    path('get_attendance_exists', views.attendance_existing, name='attendance_exists'),  # typo fixed
    path('delete_attendance',    views.delete_attendence_api, name='delete_attendence'),

    # ========== VOLUNTEER-ONLY: EXPENSES ==========
    path('expenses',                                     views.expenses,                   name='expenses'),
    path('upload_expense/<int:expense_id>',              views.upload_expense_receipt,      name='upload_expenses'),
    path('api/expenses-with-docs',                       views.get_expenses_with_documents, name='expenses_with_docs'),
    path('expenses-report',                              views.expense_report_page,         name='expense_report_page'),  # renamed: was 'report'
    path('api/download-document/<int:document_id>',      views.download_expense_document,   name='download_document'),

    # These are still kept for any existing frontend that calls them
    path('api/student-expense-summary/<int:student_id>', views.get_student_expense_summary,  name='student_expense_summary'),
    path('api/student-expenses-detail/<int:student_id>', views.get_student_expenses_with_docs, name='student_expenses_with_docs'),
    path('api/expenses-summary',                         views.get_expenses_summary,          name='expenses_summary'),

    # ========== VOLUNTEER-ONLY: VOLUNTEER PANEL ==========
    path('volunteer-panel',   views.volunteer_panel,          name='volunteer_panel'),
    path('api/generate-code', views.generate_volunteer_code,  name='generate_code'),
    path('api/get-codes',     views.get_volunteer_codes,      name='get_codes'),
    path('api/deactivate-code', views.deactivate_code,        name='deactivate_code'),

    # ========== AUTH ==========
    path('register_user', views.register_user, name='register_user'),
    path('login_user',    views.login_user,    name='login_user'),
    path('logout_user',   views.logout_user,   name='logout_user'),   # new
]
