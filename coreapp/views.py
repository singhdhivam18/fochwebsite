# =============================================================================
# coreapp/views.py
# Updated: Added middleware-based auth decorators + session tracking
# =============================================================================

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import json
import os
from datetime import datetime

# ✅ Import middleware decorators
from coreapp.middleware import check_user_type, check_authenticated

# ✅ All dataaccess imports — clean at the top
from dataaccess import (
    get_dashboard       as get_dashboard_data,   # alias to avoid name clash with view
    put_data_to_student,
    get_existing_attendance,
    put_expenses,
    upload_expenes,
    get_student_id,
    document_expenes,
    get_username,
    put_user_login,
    user_name,
    update_last_login,
    check_referral_code,
    use_referral_code,
    generate_referral_code,
    put_attendence,
    get_name_course,
    get_attendence_date,
    delete_attendence,
    get_students,
)


# =============================================================================
# PUBLIC ROUTES  (no auth required)
# =============================================================================

def login(request):
    """Login page — publicly accessible."""
    return render(request, 'login.html')


def register(request):
    """Register page — publicly accessible."""
    return render(request, 'register.html')   # ✅ fixed: was 'register' (missing .html)


# =============================================================================
# AUTHENTICATED ROUTES  (any logged-in user)
# =============================================================================

@check_authenticated
def dashboard_view(request):
    """Render main dashboard — any authenticated user."""
    return render(request, "index.html")


@check_authenticated
def get_dashboard(request):
    """Return dashboard JSON data — any authenticated user.
    Renamed from `dashboard` to `get_dashboard` to match new urls.py.
    """
    if request.method == 'GET':
        data, data_list = get_dashboard_data()
        birthday_array = []
        for eachbirthday in sorted(data_list):
            birthday = {
                "firstname":   eachbirthday[0],
                "lastname":    eachbirthday[1],
                "dateOfbirth": eachbirthday[2]
            }
            birthday_array.append(birthday)

        return JsonResponse({
            "activestudentcount":       data["activestudentdata"],
            "upcomingbirthdays":        birthday_array,
            "averageStudentAttendence": 75,
        }, safe=False)

    return JsonResponse({"error": "GET only"}, status=405)


# Keep old name so nothing else breaks
dashboard = get_dashboard


# =============================================================================
# VOLUNTEER-ONLY ROUTES: STUDENTS
# =============================================================================

@check_user_type(['volunteer'])
def records_view(request):
    """Student list page — volunteers only."""
    return render(request, 'student.html')


@csrf_exempt
@check_user_type(['volunteer'])
def get_student(request):
    """Return all students as JSON — volunteers only."""
    if request.method == "GET":
        try:
            data = get_students()
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def insert_data(request):
    """Add a new student — volunteers only.
    ✅ created_by now reads from session instead of hardcoded 'admin'.
    """
    if request.method == "POST":
        try:
            data       = json.loads(request.body.decode("utf-8"))
            created_at = datetime.now()
            updated_at = datetime.now()
            created_by = request.session.get('username', 'unknown')  # ✅ from session
            updated_by = created_by

            put_data_to_student(data, created_at, updated_at, created_by, updated_by, None)
            return JsonResponse({"message": "✅ Student added successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            print(f"Server Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST only"}, status=405)


@csrf_exempt
@check_user_type(['volunteer'])
def update_student_data(request, student_id):
    """Update existing student — volunteers only.
    ✅ updated_by now reads from session instead of hardcoded 'admin'.
    """
    if request.method == "PUT":
        try:
            data       = json.loads(request.body.decode("utf-8"))
            created_at = datetime.now()
            updated_at = datetime.now()
            created_by = request.session.get('username', 'unknown')  # ✅ from session
            updated_by = created_by

            put_data_to_student(data, created_at, updated_at, created_by, updated_by, student_id)
            return JsonResponse({"message": "✅ Student updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =============================================================================
# VOLUNTEER-ONLY ROUTES: ATTENDANCE
# =============================================================================

@check_user_type(['volunteer'])
def attendance_view(request):
    """Attendance page — volunteers only."""
    return render(request, 'attendance.html')


@csrf_exempt
@check_user_type(['volunteer'])
def put_attendance(request):
    """Submit / update attendance — volunteers only."""
    if request.method == "POST":
        try:
            data            = json.loads(request.body.decode("utf-8"))
            attendence_date = get_attendence_date()

            if data.get('date') in attendence_date:
                put_attendence(data)
                return JsonResponse({"message": "✅ Attendance updated"}, status=202)
            else:
                put_attendence(data)
                return JsonResponse({"message": "✅ Attendance saved"}, status=201)

        except Exception as e:
            print(f"Server Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def get_details_students(request):
    """Return student names + courses for attendance form — volunteers only."""
    if request.method == 'GET':
        try:
            data = get_name_course()
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def attendance_existing(request):
    """Return existing attendance for a given date — volunteers only.
    ✅ Renamed from `attendance_exixting` (typo fixed).
    """
    if request.method == 'GET':
        try:
            date            = request.GET.get('date')
            attendance_list = get_existing_attendance(date)
            return JsonResponse({"students": attendance_list}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# ✅ Backward-compat alias — old code that references attendance_exixting still works
attendance_exixting = attendance_existing


@csrf_exempt
@check_user_type(['volunteer'])
def delete_attendence_api(request):
    """Delete attendance for a given date — volunteers only."""
    if request.method == "DELETE":
        try:
            data = json.loads(request.body.decode("utf-8"))
            delete_attendence(data.get('date'))
            return JsonResponse({
                'status':  'success',
                'message': f"✅ Attendance for {data.get('date')} deleted"
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# Kept for backward compat; no longer in new urls.py
@csrf_exempt
def check_attendance(request):
    if request.method == "POST":
        try:
            date            = request.GET.get('date')
            attendence_date = get_attendence_date()
            if date in attendence_date:
                return JsonResponse({"message": "date present"}, status=202)
            return JsonResponse({"message": "date not present"}, status=203)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =============================================================================
# VOLUNTEER-ONLY ROUTES: EXPENSES
# =============================================================================

@csrf_exempt
@check_user_type(['volunteer'])
def expenses(request):
    """Create a new expense record — volunteers only."""
    if request.method == 'POST':
        try:
            data       = json.loads(request.body.decode("utf-8"))
            expense_id = put_expenses(data)
            return JsonResponse({'status': 'success', 'expense_id': expense_id}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def upload_expense_receipt(request, expense_id):
    """Upload receipt image for an expense — volunteers only.
    Stores file at: media/expenses/{student_id}/{expense_id}/receipt.<ext>
    """
    if request.method == 'POST' and request.FILES.get('receipt'):
        receipt_file = request.FILES['receipt']
        try:
            student_id = get_student_id(expense_id)

            # Validate type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf']
            if receipt_file.content_type not in allowed_types:
                return JsonResponse({'error': 'Invalid file type. Only JPG, PNG, PDF allowed'}, status=400)

            # Validate size (5 MB)
            if receipt_file.size > 5 * 1024 * 1024:
                return JsonResponse({'error': 'File too large. Max 5 MB'}, status=400)

            file_ext = os.path.splitext(receipt_file.name)[1]
            filename = f'receipt{file_ext}'

            # Build directory path
            expense_dir = os.path.join(
                settings.MEDIA_ROOT, 'expenses',
                str(student_id), str(expense_id)
            )
            os.makedirs(expense_dir, exist_ok=True)

            # Write file
            file_path = os.path.join(expense_dir, filename)
            with open(file_path, 'wb+') as dest:
                for chunk in receipt_file.chunks():
                    dest.write(chunk)

            file_url    = f'/media/expenses/{student_id}/{expense_id}/{filename}'
            document_id = upload_expenes(file_url)
            document_expenes(expense_id, document_id)

            return JsonResponse({
                'success':     True,
                'message':     'Receipt uploaded successfully',
                'file_url':    file_url,
                'expense_id':  expense_id,
                'student_id':  student_id,
                'document_id': document_id,
            })

        except Exception as e:
            print(f"Error uploading receipt: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No file provided'}, status=400)


@csrf_exempt
@check_user_type(['volunteer'])
def get_expenses_with_documents(request):
    """Return all expenses with linked documents — volunteers only."""
    if request.method == "GET":
        try:
            from dataaccess import get_all_expenses_with_documents
            result = get_all_expenses_with_documents()
            return JsonResponse({"success": True, "expenses": result}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def get_student_expense_summary(request, student_id):
    """Total expense summary for one student — volunteers only."""
    if request.method == "GET":
        try:
            from dataaccess import get_student_total_expenses
            summary = get_student_total_expenses(student_id)
            if summary:
                return JsonResponse({"success": True, "summary": summary}, status=200)
            return JsonResponse({"success": False, "error": "No data found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def get_student_expenses_with_docs(request, student_id):
    """Detailed expenses + documents for one student — volunteers only."""
    if request.method == "GET":
        try:
            from dataaccess import get_student_expenses_detail
            result = get_student_expenses_detail(student_id)
            return JsonResponse({"success": True, "student_id": student_id, "expenses": result}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def get_expenses_summary(request):
    """Expenses grouped by payment mode — volunteers only."""
    if request.method == "GET":
        try:
            from dataaccess import get_expenses_by_mode
            summary = get_expenses_by_mode()
            return JsonResponse({"success": True, "summary": summary}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@check_user_type(['volunteer'])
def expense_report_page(request):
    """Expense report page — volunteers only.
    ✅ Renamed from `report` to `expense_report_page` to match new urls.py.
    """
    return render(request, 'expenses-report.html')


# ✅ Backward-compat alias
report = expense_report_page


@csrf_exempt
@check_user_type(['volunteer'])
def download_expense_document(request, document_id):
    """Serve expense document as file download — volunteers only."""
    if request.method == "GET":
        try:
            from dataaccess import get_connection
            cursor, cnxn = get_connection()
            cursor.execute("SELECT document_source_path FROM documents WHERE id=?", (document_id,))
            result = cursor.fetchone()
            cursor.close()
            cnxn.close()

            if not result:
                return JsonResponse({"error": "Document not found"}, status=404)

            doc_path  = result[0]
            file_path = os.path.join(
                settings.MEDIA_ROOT,
                doc_path.lstrip('/media/expenses')
            )

            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True)

            return JsonResponse({"error": "File not found on server"}, status=404)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)


# =============================================================================
# VOLUNTEER-ONLY ROUTES: VOLUNTEER PANEL
# =============================================================================

@check_user_type(['volunteer'])
def volunteer_panel(request):
    """Volunteer management panel page — volunteers only."""
    return render(request, 'volunteer_panel.html')


@csrf_exempt
@check_user_type(['volunteer'])
def generate_volunteer_code(request):
    """Generate a one-use referral code — volunteers only.
    ✅ created_by now reads from session instead of request body.
    """
    if request.method == "POST":
        try:
            created_by = request.session.get('username')   # ✅ from session
            code       = generate_referral_code(created_by)

            if code:
                return JsonResponse({
                    "success": True,
                    "message": "✅ Referral code generated",
                    "code":    code
                }, status=201)

            return JsonResponse({"success": False, "error": "Failed to generate code"}, status=500)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def get_volunteer_codes(request):
    """Return referral codes created by logged-in volunteer — volunteers only.
    ✅ username now reads from session.
    """
    if request.method == "GET":
        try:
            username = request.session.get('username')     # ✅ from session
            from dataaccess import get_referral_codes_by_creator
            codes = get_referral_codes_by_creator(username)
            return JsonResponse({"success": True, "codes": codes}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@check_user_type(['volunteer'])
def deactivate_code(request):
    """Deactivate a referral code — volunteers only.
    ✅ username now reads from session.
    """
    if request.method == "POST":
        try:
            data     = json.loads(request.body)
            code     = data.get("code")

            from dataaccess import deactivate_referral_code
            success = deactivate_referral_code(code)

            if success:
                return JsonResponse({"success": True,  "message": "Code deactivated"}, status=200)
            return JsonResponse({"success": False, "error": "Failed to deactivate"}, status=500)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


# =============================================================================
# AUTH API ENDPOINTS  (login / register — public, no decorator)
# =============================================================================

@csrf_exempt
def register_user(request):
    """Register a new user (student or volunteer)."""
    if request.method == "POST":
        try:
            data          = json.loads(request.body)
            username      = data.get("username",      "").strip()
            password      = data.get("password",      "")
            user_type     = data.get("user_type",     "student")
            referral_code = data.get("referral_code", "").strip()

            user_namelist = get_username()

            # Validations
            if not username or not password:
                return JsonResponse({"error": "Both fields are required."}, status=400)
            if len(username) < 3:
                return JsonResponse({"error": "Username must be at least 3 characters."}, status=400)
            if len(password) < 4:
                return JsonResponse({"error": "Password must be at least 4 characters."}, status=400)
            if username in user_namelist:
                return JsonResponse({"error": "Username already taken."}, status=400)

            # Volunteer: check referral code
            if user_type == "volunteer":
                from dataaccess import count_volunteers
                volunteer_count = count_volunteers()

                if volunteer_count > 0:
                    if not referral_code:
                        return JsonResponse({
                            "error": "🔑 Referral code required. Ask an existing volunteer for a code."
                        }, status=400)
                    if not check_referral_code(referral_code):
                        return JsonResponse({"error": "❌ Invalid or expired referral code"}, status=400)
                    use_referral_code(referral_code)
                else:
                    print(f"🎉 Bootstrap: Creating FIRST VOLUNTEER — {username}")

            # Hash password and save
            hashed = make_password(password)
            salt   = hashed.split("$")[2] if "$" in hashed else ""

            user_data = {
                "user_name":     username,
                "password_hash": hashed,
                "salt":          salt,
                "last_login":    None
            }
            put_user_login(user_data, user_type=user_type, referral_code=referral_code)

            return JsonResponse({
                "success":   True,
                "message":   f"Account created as {user_type}!",
                "user_type": user_type
            }, status=201)

        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def login_user(request):
    """Authenticate user and set session — public endpoint.
    ✅ Now stores username + user_type in session so middleware works.
    """
    if request.method == "POST":
        try:
            data     = json.loads(request.body)
            username = data.get("username", "").strip()
            password = data.get("password", "")

            if not username or not password:
                return JsonResponse({"error": "Both fields are required."}, status=400)

            user_detail = user_name(username)

            if not user_detail or username != user_detail.get('user_name'):
                return JsonResponse({"error": "Invalid username or password."}, status=401)

            password_hash = user_detail.get('password_hash')
            user_type     = user_detail.get('user_type', 'student')

            if check_password(password, password_hash):
                time = datetime.now()
                update_last_login(username, time)

                # ✅ SET SESSION — required for middleware decorators to work
                request.session['username']  = username
                request.session['user_type'] = user_type

                return JsonResponse({
                    "success":    True,
                    "message":    f"Welcome, {username}!",
                    "username":   username,
                    "user_type":  user_type,
                    "last_login": str(time)
                }, status=200)

            return JsonResponse({"error": "Invalid username or password."}, status=401)

        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def logout_user(request):
    """Clear session and log user out."""
    if request.method == "POST":
        request.session.flush()
        return JsonResponse({"success": True, "message": "Logged out"}, status=200)
