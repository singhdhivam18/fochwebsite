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
from dataaccess import get_dashboard,put_data_to_student,get_existing_attendance,put_expenses,upload_expenes,get_student_id,document_expenes,get_username,put_user_login,user_name,update_last_login
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




@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
    try:
        username = data.get("username", "").strip()   #  strip username
        password = data.get("password", "")           #  never strip password
        user_namelist=get_username()
        if not username or not password:
            return JsonResponse({"error": "Both fields are required."}, status=400)

        if len(username) < 3:
            return JsonResponse({"error": "Username must be at least 3 characters."}, status=400)

        if len(password) < 4:
            return JsonResponse({"error": "Password must be at least 4 characters."}, status=400)

        if username in user_namelist:
            return JsonResponse({"error": "Username already taken."}, status=400)

        # make_password() generates the salt and embeds it inside the hash string
        # format:  algorithm$salt$hash  e.g.  pbkdf2_sha256$720000$abc123$xyz...
        hashed = make_password(password)

        # we store the full hash string in password_hash
        # and optionally extract + store the salt separately in the salt column
        salt = hashed.split("$")[2] if "$" in hashed else ""

        data={
            "user_name":username,
            "password_hash":hashed,
            "salt"          :salt,     
            "last_login" :None
        }
        put_user_login(data)
        return JsonResponse({"success": True, "message": "Account created."}, status=201)
    except Exception as e:
            print(f"Error uploading receipt: {e}")
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username", "").strip()   # strip username
        password = data.get("password", "")           # never strip password

        if not username or not password:
            return JsonResponse({"error": "Both fields are required."}, status=400)

        data_list=user_name(username)
        print(data_list[0][0])
        print(username)
        if username==data_list[0][0]:
            password_hash=data_list[0][1]
        # check_password() re-hashes the input using the salt inside password_hash
        # and compares — returns True or False
            #print(password,password_hash)
            #print(check_password(password,password_hash))
            if check_password(password,password_hash):
                time=datetime.now()
                update_last_login(username,time)
                return JsonResponse({
                        "success"   : True,
                        "message"   : f"Welcome, {username}!",
                        "username"  : username,
                        "last_login": str(time)
                })
        else:
            return JsonResponse({"error": "Invalid username or password."}, status=401)