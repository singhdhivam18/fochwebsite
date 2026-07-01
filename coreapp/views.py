from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from datetime import datetime
import decimal

'''# Create your views here.
def myself(request):
    if request.method=='GET':    
        return HttpResponse("hi iam shivam")
def index(request):
    return render(request,'index.html')
def about(request):
    return HttpResponse("this is about")'''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from dataaccess import (
    get_dashboard, put_data_to_student, get_existing_attendance, 
    put_expenses, upload_expenes, get_student_id, document_expenes, 
    get_username, put_user_login, user_name, update_last_login,
    check_referral_code, use_referral_code, generate_referral_code  
)
from datetime import datetime

'''@csrf_exempt
def register(request):
    if request.method=='GET':
        id_value=request.GET.get('id')
        if id_value is None:
            return JsonResponse({"error not given "},status=400)
        #studentdata=get_studentData(id_value)
        for student in studentdata:
            return [{"id":student[0],"firstname":student[1],"lastname":student[2],"fathername":student[3],"mothername":student[4],"DOB":student[5],"status":student[6] }]'''
         
def dashboard_view(request):
    return render(request, "index.html")
def records_view(request):
    return render(request, 'student.html')
def attendance_view(request):
    return render(request, 'attendance.html')
def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register')
def volunteer_panel(request):
    return render(request,'volunteer_panel.html')
def report(request):
    return render(request,'expenses-report.html')
def dashboard(request):
    if request.method=='GET':
        data,data_list=get_dashboard()
        birthday_array=[]
        for eachbirthday in sorted(data_list):
            
            
            birthday={
                    "firstname":eachbirthday[0],
                    "lastname":eachbirthday[1],
                    "dateOfbirth":eachbirthday[2]
            }
            birthday_array.append(birthday)
        '''def make_take_decimal(value):
            if isinstance(value,decimal.Decimal):
                value=float(value)
            return value[0]        
        expenses_array=[]
        
        for key,value in expenses_dict.items():
           
            expenses_json={
                "horizontalvalue":key,
                "verticalvalue":make_take_decimal(value[0][0])
            }
            expenses_array.append(expenses_json)
        student_data=[]
        for key,value in student_wise_data.items():
           
                studentWisedata={
                    "horizontalvalue":key,
                    "verticalvalue":value
                }
                student_data.append(studentWisedata)
        group_data=[]
        for key,value in group_dict.items():
           
                groupWisedata={
                    "horizontalvalue":key,
                    "verticalvalue":value
                }
                group_data.append(groupWisedata)
                '''
        return JsonResponse({
            "activestudentcount":data["activestudentdata"],
            "upcomingbirthdays":birthday_array,
            "averageStudentAttendence":75,
            
            },safe=False)
    else:
        return JsonResponse("fail")

import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dataaccess import put_data_to_student,put_attendence,get_name_course,get_attendence_date,delete_attendence
# Use csrf_exempt if you are testing via Postman or not sending the CSRF token from frontend
@csrf_exempt
def insert_data(request):
    if request.method == "POST":
        try:
            # 1. Parse the JSON body
            # This is the correct line you asked about
            data = json.loads(request.body.decode("utf-8"))
            print("i am",data)
            # 2. Prepare timestamps and user info
            created_at = datetime.now()
            updated_at = datetime.now()
            created_by, updated_by = ('admin', 'admin') # Hardcoded for now
            # 3. Call your database function
            put_data_to_student(data, created_at, updated_at, created_by, updated_by,None)
            
            return JsonResponse({"message": "Data stored successfully"}, status=201)

        except json.JSONDecodeError:
            # Catches errors if the Body is empty or bad JSON
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
            
        except Exception as e:
            # Catches database errors or other code failures
            print(f"Server Error: {e}") # Print error to console for debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    
    else:
        # Handles GET, PUT, DELETE etc.
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)
@csrf_exempt
def update_student_data(request,student_id):
    if request.method == "PUT":
        try:
            # 1. Parse the JSON body
            # This is the correct line you asked about
            data = json.loads(request.body.decode("utf-8"))
            created_at = datetime.now()
            updated_at = datetime.now()
            created_by, updated_by = ('admin', 'admin')
            put_data_to_student(data, created_at, updated_at, created_by, updated_by,student_id)
            
            return JsonResponse({"message": "Data stored successfully"}, status=201)

        except json.JSONDecodeError:
            # Catches errors if the Body is empty or bad JSON
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
            
from dataaccess import get_students
@csrf_exempt
def get_student(request):
    if request.method=="GET":
        try:
            data=get_students()
            return JsonResponse(data, safe=False) # safe=False allows returning a list
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
from django.views.decorators.csrf import csrf_exempt     
@csrf_exempt
def put_attendance(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body.decode("utf-8"))
            attendence_date=get_attendence_date()
            print(data.get('date'),attendence_date)
            if data.get('date') in attendence_date:
                put_attendence(data)
                return JsonResponse({"message": "updated successfully ! "}, status=202)
            else:
                put_attendence(data)
                return JsonResponse({"message": "Data stored successfully"}, status=201)
        except Exception as e:
            # Catches database errors or other code failures
            print(f"Server Error: {e}") # Print error to console for debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
from django.views.decorators.csrf import csrf_exempt     
def get_details_students(request):
    if request.method=='GET':
        try:
            data=get_name_course()
            return JsonResponse(data,safe=False)
        except Exception as e:
            # Catches database errors or other code failures
            print(f"Server Error: {e}") # Print error to console for debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt     
def delete_attendence_api(request):
    if request.method=="DELETE":
        try:
            data=json.loads(request.body.decode("utf-8"))
            delete_attendence(data.get('date'))
            return JsonResponse({
                'status': 'success',
                'message': f'Attendance for {data.get('date')} deleted successfully'
            }, status=200)
            
        except Exception as e:
            # Catches database errors or other code failures
            print(f"Server Error: {e}") # Print error to console for debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
        
@csrf_exempt    
def attendance_exixting(request):
    if request.method=='GET':
        try:
            data=request.GET.get('date')
            attendance_list=get_existing_attendance(data)
            return JsonResponse({"students":attendance_list
            }, status=200)
        except Exception as e:
            # Catches database errors or other code failures
            print(f"Server Error: {e}") # Print error to console for debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
@csrf_exempt      
def check_attendance(request):
    if request.method=="POST":
        try:
            data=request.GET.get('date')
            print("date",data)
            attendence_date=get_attendence_date()
            print("attendance",attendence_date)
            if data in attendence_date:
                return JsonResponse({"message": "date present with date successfully ! "}, status=202)
            else:
                return JsonResponse({"message": "date present successfully ! "}, status=203)
        except Exception as e:
            # Catches database errors or other code failures
            print(f"Server Error: {e}") # Print error to console for debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

@csrf_exempt
def expenses(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body.decode("utf-8"))
            expense_id=put_expenses(data)
            return JsonResponse({
                'status': 'success',
                'message': f'sucessfully',
                "expense_id":expense_id
            }, status=200)
            
        except Exception as e:
            # Catches database errors or other code failures
            print(f"Server Error: {e}") # Print error to console for debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
        
import os
from django.conf import settings    
@csrf_exempt
def upload_expense_receipt(request, expense_id):
    """
    Upload receipt file for expense - SECURE VERSION
    POST /api/upload-expense-receipt/<expense_id>
    FormData: {receipt: file, student_id: int}
    Returns: {file_url}
    """
    if request.method == 'POST' and request.FILES.get('receipt'):
        receipt_file = request.FILES['receipt']
        
        try:
            student_id=get_student_id(expense_id)
            # Validate file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf']
            if receipt_file.content_type not in allowed_types:
                return JsonResponse({
                    'error': 'Invalid file type. Only JPG, PNG, and PDF allowed'
                }, status=400)
            
            # Validate file size (5MB)
            if receipt_file.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'error': 'File too large. Maximum size is 5MB'
                }, status=400)
            
            # Get file extension
            file_ext = os.path.splitext(receipt_file.name)[1]
            
            # SECURE: Construct path from validated data (not user input)
            filename = f'receipt{file_ext}'
            
            # Create directory: media/expenses/{student_id}/{expense_id}/
            expense_dir = os.path.join(
                settings.MEDIA_ROOT,
                'expenses',
                str(student_id),
                str(expense_id)
            )
            os.makedirs(expense_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(expense_dir, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in receipt_file.chunks():
                    destination.write(chunk)
            
            
            # Construct safe URL for response
            file_url = f'/media/expenses/{student_id}/{expense_id}/{filename}'
            document_id=upload_expenes(file_url)
            document_expenes(expense_id,document_id)
            return JsonResponse({
                'success': True,
                'message': 'Receipt uploaded successfully',
                'file_url': file_url,
                'expense_id': expense_id,
                'student_id': student_id,
                'document_id':document_id,
            })
            
        except Exception as e:
            print(f"Error uploading receipt: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'No file provided'}, status=400)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
# ✅ REPLACE register_user function
@csrf_exempt
def register_user(request):
    """Register new user (student or volunteer)"""
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            username = data.get("username", "").strip()
            password = data.get("password", "")
            user_type = data.get("user_type", "student")
            referral_code = data.get("referral_code", "").strip()
            
            user_namelist = get_username()
            
            # ✅ VALIDATIONS
            if not username or not password:
                return JsonResponse({"error": "Both fields are required."}, status=400)

            if len(username) < 3:
                return JsonResponse({"error": "Username must be at least 3 characters."}, status=400)

            if len(password) < 4:
                return JsonResponse({"error": "Password must be at least 4 characters."}, status=400)

            if username in user_namelist:
                return JsonResponse({"error": "Username already taken."}, status=400)

            # 🎯 VOLUNTEER LOGIC: Check if bootstrap needed
            if user_type == "volunteer":
                from dataaccess import count_volunteers
                
                volunteer_count = count_volunteers()
                
                # If volunteers exist, REQUIRE code
                if volunteer_count > 0:
                    if not referral_code:
                        return JsonResponse({
                            "error": "🔑 Referral code required. Ask an existing volunteer for a code."
                        }, status=400)
                    
                    # Validate code
                    if not check_referral_code(referral_code):
                        return JsonResponse({
                            "error": "❌ Invalid or expired referral code"
                        }, status=400)
                    
                    # Mark code as used
                    use_referral_code(referral_code)
                    print(f"✅ Referral code used: {referral_code}")
                else:
                    # First volunteer - no code needed
                    print(f"🎉 Bootstrap: Creating FIRST VOLUNTEER - {username}")

            # ✅ Hash password
            hashed = make_password(password)
            salt = hashed.split("$")[2] if "$" in hashed else ""
            
            user_data = {
                "user_name": username,
                "password_hash": hashed,
                "salt": salt,
                "last_login": None
            }
            
            # ✅ Save user
            put_user_login(user_data, user_type=user_type, referral_code=referral_code)
            
            return JsonResponse({
                "success": True, 
                "message": f"Account created as {user_type}!",
                "user_type": user_type
            }, status=201)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

# ✅ login_user — issues a JWT cookie (no Django session / ORM needed)
import jwt as pyjwt
from datetime import timezone, timedelta
from django.conf import settings as django_settings

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username", "").strip()
            password = data.get("password", "")

            if not username or not password:
                return JsonResponse({"error": "Both fields are required."}, status=400)

            # Fetch user from your raw MSSQL query
            user_detail = user_name(username)

            if not user_detail or username != user_detail.get('user_name'):
                return JsonResponse({"error": "Invalid username or password."}, status=401)

            password_hash = user_detail.get('password_hash')
            user_type     = user_detail.get('user_type', 'student')

            if check_password(password, password_hash):
                login_time = datetime.now()          # local time — for DB last_login display
                update_last_login(username, login_time)

                # ── Build JWT payload (MUST use UTC, not local time) ───────
                # PyJWT validates 'iat'/'exp' against UTC. If we use local
                # time (e.g. IST = UTC+5:30) the token looks "issued in the
                # future" to PyJWT and gets rejected with
                # ImmatureSignatureError: The token is not yet valid (iat)
                utc_now = datetime.now(timezone.utc)
                payload = {
                    'username':  username,
                    'user_type': user_type,
                    'iat':       utc_now,
                    'exp':       utc_now + timedelta(hours=8),
                }
                token = pyjwt.encode(
                    payload,
                    django_settings.JWT_SECRET_KEY,
                    algorithm='HS256'
                )
                # ──────────────────────────────────────────────────────────

                response = JsonResponse({
                    "success":    True,
                    "message":    f"Welcome, {username}!",
                    "username":   username,
                    "user_type":  user_type,
                    "last_login": str(login_time)
                }, status=200)

                # ── Set JWT as HttpOnly cookie (JS cannot read/steal it) ───
                response.set_cookie(
                    key='foch_token',
                    value=token,
                    max_age=8 * 3600,   # 8 hours in seconds
                    httponly=True,      # not accessible from JavaScript
                    samesite='Lax',    # CSRF protection
                    secure=False,       # set True when deploying on HTTPS
                )
                return response
            else:
                return JsonResponse({"error": "Invalid username or password."}, status=401)

        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def logout_user(request):
    """Delete the JWT cookie — no DB interaction needed."""
    response = JsonResponse({"success": True, "message": "Logged out successfully."}, status=200)
    response.delete_cookie('foch_token')
    return response

# ✅ NEW: Generate referral code (for volunteers only)
@csrf_exempt
def generate_volunteer_code(request):
    """Volunteers can generate referral codes for new volunteers"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            created_by = data.get("username")  # Current logged-in user
            
            # Verify user is a volunteer
            user_detail = user_name(created_by)
            if not user_detail or user_detail.get('user_type') != 'volunteer':
                return JsonResponse({"error": "Only volunteers can generate codes"}, status=403)
            
            # Generate code
            code = generate_referral_code(created_by)
            
            return JsonResponse({
                "success": True,
                "message": "Referral code generated",
                "code": code
            }, status=201)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
def generate_volunteer_code(request):
    """Volunteers can generate referral codes for new volunteers"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            created_by = data.get("username")  # Current logged-in volunteer
            
            # Verify user is a volunteer
            user_data = user_name(created_by)
            if not user_data or user_data.get('user_type') != 'volunteer':
                return JsonResponse({
                    "success": False,
                    "error": "Only volunteers can generate codes"
                }, status=403)
            
            # Generate code
            code = generate_referral_code(created_by)
            
            if code:
                return JsonResponse({
                    "success": True,
                    "message": "Referral code generated",
                    "code": code
                }, status=201)
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Failed to generate code"
                }, status=500)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# ✅ NEW: Get all codes for a volunteer
@csrf_exempt
def get_volunteer_codes(request):
    """Get all referral codes created by logged-in volunteer"""
    if request.method == "GET":
        try:
            username = request.GET.get("username")
            
            # Verify user is a volunteer
            user_data = user_name(username)
            if not user_data or user_data.get('user_type') != 'volunteer':
                return JsonResponse({
                    "success": False,
                    "error": "Only volunteers can view codes"
                }, status=403)
            
            # Get codes
            from dataaccess import get_referral_codes_by_creator
            codes = get_referral_codes_by_creator(username)
            
            return JsonResponse({
                "success": True,
                "codes": codes
            }, status=200)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# ✅ NEW: Volunteer panel page
def volunteer_panel(request):
    """Render volunteer management panel"""
    return render(request, 'volunteer_panel.html')

# ✅ NEW: Deactivate code
@csrf_exempt
def deactivate_code(request):
    """Deactivate a referral code"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code")
            username = data.get("username")
            
            # Verify user is a volunteer
            user_data = user_name(username)
            if not user_data or user_data.get('user_type') != 'volunteer':
                return JsonResponse({
                    "success": False,
                    "error": "Not authorized"
                }, status=403)
            
            # Deactivate code
            from dataaccess import deactivate_referral_code
            success = deactivate_referral_code(code)
            
            if success:
                return JsonResponse({
                    "success": True,
                    "message": "Code deactivated"
                }, status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Failed to deactivate"
                }, status=500)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# ✅ Get all expenses with documents
@csrf_exempt
def get_expenses_with_documents(request):
    """Get all expenses with linked documents"""
    if request.method == "GET":
        try:
            from dataaccess import get_all_expenses_with_documents
            expenses = get_all_expenses_with_documents()
            
            return JsonResponse({
                "success": True,
                "expenses": expenses
            }, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# ✅ Get student expense summary
@csrf_exempt
def get_student_expense_summary(request, student_id):
    """Get total expense summary for a student"""
    if request.method == "GET":
        try:
            from dataaccess import get_student_total_expenses
            summary = get_student_total_expenses(student_id)
            
            if summary:
                return JsonResponse({
                    "success": True,
                    "summary": summary
                }, status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "error": "No data found"
                }, status=404)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# ✅ Get student expenses with documents
@csrf_exempt
def get_student_expenses_with_docs(request, student_id):
    """Get detailed expenses for student with documents"""
    if request.method == "GET":
        try:
            from dataaccess import get_student_expenses_detail
            expenses = get_student_expenses_detail(student_id)
            
            return JsonResponse({
                "success": True,
                "student_id": student_id,
                "expenses": expenses
            }, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# ✅ Get expense summary by mode
@csrf_exempt
def get_expenses_summary(request):
    """Get expenses grouped by payment mode"""
    if request.method == "GET":
        try:
            from dataaccess import get_expenses_by_mode
            summary = get_expenses_by_mode()
            
            return JsonResponse({
                "success": True,
                "summary": summary
            }, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# ✅ Download expense document
@csrf_exempt
def download_expense_document(request, document_id):
    """Download expense receipt document"""
    if request.method == "GET":
        try:
            import os
            from django.conf import settings
            from django.http import FileResponse
            
            # Get document path from database
            from dataaccess import get_connection
            cursor, cnxn = get_connection()
            cursor.execute("SELECT document_source_path FROM documents WHERE id=?", (document_id,))
            result = cursor.fetchone()
            cursor.close()
            cnxn.close()
            
            if not result:
                return JsonResponse({"error": "Document not found"}, status=404)
            
            doc_path = result[0]
            file_path = os.path.join(settings.MEDIA_ROOT, doc_path.lstrip('/media/expenses'))
            
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True)
            else:
                return JsonResponse({"error": "File not found"}, status=404)
        
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)