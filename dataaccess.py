import pyodbc
from getconnectionstring import connectionstring
import datetime
import json
import calendar
import decimal
import uuid

def get_connection():
        
        try:
                cnxn = pyodbc.connect(connectionstring)
                print("Connected to the database!")
                return cnxn.cursor(), cnxn
        except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                if sqlstate == 'HY000':
                        print(f"Connection failed: {ex}")
                else:
                        print(f"An error occurred: {ex}")
                exit()




def get_dashboard():
    cursor, cnxn = get_connection()
    current_date = datetime.date.today()
    current_month_name = current_date.strftime('%B')
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    month_end_date = datetime.date(current_date.year, current_date.month, last_day)

    data = {}
    birthday_list = []

    try:
        # 1️⃣ Active student count
        cursor.execute("""
            SELECT COUNT(*) 
            FROM students 
            WHERE is_active=1
        """)
        activestudentresult = cursor.fetchone()
        activestudent = activestudentresult[0] if activestudentresult else 0
        data["activestudentdata"] = activestudent

        # 2️⃣ Birthdays in current month
        cursor.execute("""
            SELECT first_name, last_name, date_of_birth 
            FROM students 
            WHERE MONTH(date_of_birth) = ? 
              AND DAY(date_of_birth) BETWEEN ? AND ?
        """, (current_date.month, current_date.day, month_end_date.day))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                birthday_list.append([row.first_name, row.last_name, row.date_of_birth])

        '''# 3️⃣ Top students by amount
        cursor.execute("""
            SELECT first_name, SUM(amount) AS total_amount 
            FROM payments 
            GROUP BY first_name 
            ORDER BY total_amount DESC
        """)'''
        '''student_dict = {}
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                student_dict[row.first_name] = row.total_amount
            sorted_dict_desc = dict(sorted(student_dict.items(), key=lambda item: item[1], reverse=True))
            data["top_students"] = sorted_dict_desc

        # 4️⃣ Group-wise expenses
        cursor.execute("""
            SELECT expense_type, SUM(cost) AS total_cost 
            FROM expenses 
            WHERE YEAR(expense_date) = ? 
            GROUP BY expense_type
        """, (current_date.year,))
        rows = cursor.fetchall()
        groupWisedict = {}
        if rows:
            for row in rows:
                groupWisedict[row.expense_type] = row.total_cost
            data["groupwise_expenses"] = groupWisedict'''

    except pyodbc.ProgrammingError as e:
        print("Programming error occurred:", e)
    finally:
        cnxn.commit()
        cursor.close()
        cnxn.close()

    return data, birthday_list

def get_attendence_date():
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data received database")
    
    try:
        query_attendence_date="""  select attendence_date from attendence"""
        cursor.execute(query_attendence_date)
        row=cursor.fetchall()
        attendence_date=[]
        for (date_val,) in row:
            attendence_date.append(date_val.strftime("%Y-%m-%d"))
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()     
    return attendence_date
def delete_attendence(date):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data received database")
    try:
        query_attendence_date="""delete from attendence where attendence_date=?"""
        cursor.execute(query_attendence_date,date)
        cnxn.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()

def put_data_to_student(data, created_at, updated_at, created_by, updated_by,student_id):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data received from frontend: {data}")
    try:
        # 1. Use INSERT INTO, not SELECT
        # 2. Add 'support_type' and 'address_location' if they exist in your DB columns
        query = """
            INSERT INTO students (
                first_name, last_name, date_of_birth, gender, created_at, created_by,
                updated_at, updated_by, is_active, is_delete, father_name, mother_name,
                parent_contact_number, student_contact_number, address, course_pursing,address_location,
                family_source_of_income, family_monthly_income, residential_status,
                additional_assets, total_monthly_average_expense_siblings,
                family_member_count, date_of_joining, support_type,studying_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """

        params = (
            data.get("first_name"), data.get("last_name"), data.get("date_of_birth") or None,
            data.get("gender"), created_at, created_by, updated_at, updated_by,
            1 if data.get("is_active") else 0, 1 if data.get("is_delete") else 0,
            data.get("father_name"), data.get("mother_name"), data.get("parent_contact_no"),
            data.get("student_contact_no"), data.get("address"), data.get("course_pursing"),data.get("address_location"),
            data.get("family_source_of_income"), data.get("family_monthly_income") or 0,
            data.get("residentail_status"), data.get("additional_assets"),
            data.get("total_montly_average") or 0, data.get("family_member_count") or 0,
            data.get("date_of_joining") or None, data.get("support") or None,data.get("study_at")
        )
        query_check="""select id from students where is_active=1"""
        cursor.execute(query_check)
        row=cursor.fetchall()
        student_id_list=[]
        for (std_id,) in row:
            student_id_list.append(std_id)
        print(student_id_list,student_id)
        if student_id in student_id_list:
            query_update= """
            update students set
                first_name=?, last_name=?, date_of_birth=?, gender=?, created_at=?, created_by=?,
                updated_at=?, updated_by=?, is_active=?, is_delete=?, father_name=?, mother_name=?,
                parent_contact_number=?, student_contact_number=?, address=?, course_pursing=?,address_location=?,
                family_source_of_income=?, family_monthly_income=?, residential_status=?,
                additional_assets=?, total_monthly_average_expense_siblings=?,
                family_member_count=?, date_of_joining=?, support_type=?,studying_at=?
                where id=?;
            """
            params = (
            data.get("first_name"), data.get("last_name"), data.get("date_of_birth") or None,
            data.get("gender"), created_at, created_by, updated_at, updated_by,
            1 if data.get("is_active") else 0,1 if data.get("is_delete") else 0,
            data.get("father_name"), data.get("mother_name"), data.get("parent_contact_number"),
            data.get("student_contact_no"), data.get("address"), data.get("course_pursing"),data.get("address_location"),
            data.get("family_source_of_income"), data.get("family_monthly_income") or 0,
            data.get("residential_status"), data.get("additional_assets"),
            data.get("total_monthly_average_expense_siblings") or 0, data.get("family_member_count") or 0,
            data.get("date_of_joining") or None, data.get("support_type") or None,data.get("studying'3_at"),student_id
            )
            cursor.execute(query_update, params)
            cnxn.commit() # THIS SAVES THE DATA
            print("--- DATA UPDATED AND COMMITTED ---")

        elif(student_id==None):
            print("i came")
            cursor.execute(query, params)
            cnxn.commit() # THIS SAVES THE DATA
            print("--- DATA INSERTED AND COMMITTED ---")

    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()

def get_students():
    cursor, cnxn = get_connection()
    students_list = []
    
    try:
        # Select all columns matching your SQL schema
        query = """
                SELECT id, first_name, last_name, date_of_birth, gender, 
                   is_active, father_name, mother_name, parent_contact_number, 
                   student_contact_number, address, course_pursing, address_location, 
                   family_source_of_income,family_monthly_income,residential_status,additional_assets,total_monthly_average_expense_siblings,family_member_count, date_of_joining, support_type, studying_at 
            FROM students
            ORDER BY id ASC
        """
        cursor.execute(query)
        columns = [column[0] for column in cursor.description] # Get column names
        rows = cursor.fetchall()

        for row in rows:
            student = dict(zip(columns, row))
            
            # Convert dates to strings (JSON cannot handle date objects)
            for key, value in student.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    student[key] = value.isoformat()
            
            students_list.append(student)
        
    except Exception as e:
        print(f"Error fetching students: {e}")
    finally:
        cursor.close()
        cnxn.close()
    return students_list

def put_attendence(data):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data received from frontend: {data}")
   
    try:
        attendance_data=get_attendence_date()
        date=data.get('date')
        if date in attendance_data:
            query_update="""UPDATE attendence SET has_attendence = ? where attendence_date= ? and student_id=?"""
            for data_dict in data.get('records'):
                has_attendance=data_dict.get('status')
                if(has_attendance=='present'):
                    status=1
                else:
                    status=0
                params=(status,data.get('date'),data_dict.get('studentId'))
                cursor.execute(query_update,params)
                cnxn.commit()
        else:    
            query="""INSERT INTO attendence( has_attendence,attendence_date,inserted_at,inserted_by,student_id) 
                    values (?,?,?,?,?)"""
            for data_dict in data.get('records'):
                has_attendance=data_dict.get('status')
                if(has_attendance=='present'):
                    status=1
                else:
                    status=0
                params=(status,data.get('date'),datetime.datetime.now(),'admin',data_dict.get("studentId"))
                cursor.execute(query,params)
                cursor.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()        

def get_name_course():
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data received from frontend:")
    students_list=[]
    try:
        query="""select id,first_name,last_name,course_pursing from students where is_active=1"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]# Get column names
        row=cursor.fetchall()
        for rows in row:
            student = dict(zip(columns, rows))
            
            # Convert dates to strings (JSON cannot handle date objects)
            for key, value in student.items():
                student[key] = value
            students_list.append(student)
        print(students_list)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()     
    return students_list

def get_existing_attendance(date):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data recevied from database attendence :")
    attendance_list=[]
    try:
        query="""select s.id,s.first_name,s.last_name,a.has_attendence,s.course_pursing from attendence a JOIN students s ON a.student_id=s.id 
        where a.attendence_date= ? """
        cursor.execute(query,date)
        columns = [column[0] for column in cursor.description]# Get column names
        row=cursor.fetchall()
        
        for rows in row:
            attendance= dict(zip(columns, rows))
            
            # Convert dates to strings (JSON cannot handle date objects)
            for key, value in attendance.items():
                attendance[key] = value
            
            attendance_list.append(attendance)
            print(attendance_list)
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()     
    return attendance_list
"""put expenses to the database get the data from the frontend"""
def put_expenses(data):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data recevied from database expenses:")
    try:
        unique_id=str(uuid.uuid4())
        query="""INSERT INTO expenses(voucher_number,created_at,created_by,updated_at,updated_by,is_active,is_deleted,expense_type,amount,currency,accounting_year,remark_expenses,student_id,mode_of_payment) OUTPUT INSERTED.id values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        params=(unique_id ,datetime.datetime.now(),'admin',datetime.datetime.now(),'admin',1,0,'student',data.get('amount'),'rup','2025-26',data.get('remark'),data.get('student_id'),data.get('mode_of_payment'))
        cursor.execute(query,params)
        
        expense_id = cursor.fetchone()[0]
        cursor.commit()
        print('data stored successfully')
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()     
        return expense_id
    
def get_student_id(expenses_id):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data recevied from database expenses:")
    try:
        cursor.execute("""
                SELECT student_id 
                FROM expenses 
                WHERE id = ?
            """, (expenses_id,))
            
        result = cursor.fetchone()
            
        if not result:
                print("expenes not found")
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()     
        return result[0]#student_id
    
def upload_expenes(file_url):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data recevied from database expenses:")
    try:
        query="""INSERT INTO documents(document_source_type,document_source_path,created_at,created_by,updated_at,updated_by,is_active,is_deleted)OUTPUT INSERTED.id VALUES (?,?,?,?,?,?,?,?)"""
        params=('jpg',file_url,datetime.datetime.now(),'admin',datetime.datetime.now(),'admin',1,0)
        cursor.execute(query,params)
        document_id=cursor.fetchone()[0]
        cursor.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close() 
        return  document_id
    
def document_expenes(expense_id,document_id):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data recevied from database expenses:")
    try:
        query="""INSERT INTO expense_documents(expense_id,document_id,created_at,created_by,updated_at,updated_by,is_active,is_delete,document_type) VALUES (?,?,?,?,?,?,?,?,?)"""
        params=(expense_id,document_id,datetime.datetime.now(),'admin',datetime.datetime.now(),'admin',1,0,'jpg')
        cursor.execute(query,params)
        cursor.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close() 
        
def get_username():
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data recevied from database attendence :")
    username_list=[]
    try:
        query="""select (user_name) from user_login"""
        cursor.execute(query)
        row=cursor.fetchall()
        
        for (rows,) in row:
            username_list.append(rows)
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()     
    return username_list

def put_user_login(data, user_type='student', referral_code=None):
    """Insert new user with user_type and referral code"""
    cursor, cnxn = get_connection()
    print(f"DEBUG: Creating {user_type} user: {data}")
    try:
        query = """
            INSERT INTO user_login(
                user_name, password_hash, salt, is_active, 
                created_at, updated_at, last_login, user_type, referral_code_used
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data.get("user_name"), 
            data.get("password_hash"), 
            data.get("salt"),
            1, 
            datetime.datetime.now(), 
            datetime.datetime.now(), 
            datetime.datetime.now(), 
            user_type, 
            referral_code
        )
        cursor.execute(query, params)
        cnxn.commit()
        print('✅ User created successfully')
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()
def update_last_login(username,time):
    cursor, cnxn = get_connection()
    print(f"DEBUG: Data recevied from database expenses:")
    try:
        query="""UPDATE user_login SET last_login = ? where user_name= ? """
        params=(time,username)
        cursor.execute(query,params)
        
        cursor.commit()
        print('data stored successfully')
    except Exception as e:
        print(f"Error occurred: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()   
# ✅ MODIFY existing user_name function to return user_type
def user_name(username):
    """Get user details including user_type"""
    cursor, cnxn = get_connection()
    print(f"DEBUG: Fetching user: {username}")
    user_detail = {}
    try:
        query = """
            SELECT user_name, password_hash, user_type, referral_code_used 
            FROM user_login 
            WHERE user_name=?
        """
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        if row:
            user_detail = {
                'user_name': row.user_name,
                'password_hash': row.password_hash,
                'user_type': row.user_type if row.user_type else 'student',
                'referral_code_used': row.referral_code_used
            }
    except Exception as e:
        print(f"❌ Error occurred: {e}")
    finally:
        cursor.close()
        cnxn.close()
    return user_detail

def check_referral_code(code):
    """✅ Check if referral code is valid and has uses left"""
    cursor, cnxn = get_connection()
    try:
        query = """
            SELECT id, times_used, max_uses FROM volunteer_referral_codes 
            WHERE referral_code=? AND is_active=1 
            AND times_used < max_uses
        """
        cursor.execute(query, (code,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking referral code: {e}")
        return False
    finally:
        cursor.close()
        cnxn.close()

def use_referral_code(code):
    """✅ Increment usage count of referral code"""
    cursor, cnxn = get_connection()
    try:
        query = """
            UPDATE volunteer_referral_codes 
            SET times_used = times_used + 1 
            WHERE referral_code=?
        """
        cursor.execute(query, (code,))
        cnxn.commit()
    except Exception as e:
        print(f"Error using referral code: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()

def generate_referral_code(created_by):
    """✅ Generate new referral code for volunteers"""
    cursor, cnxn = get_connection()
    try:
        code = f"VOL-{uuid.uuid4().hex[:8].upper()}"
        query = """
            INSERT INTO volunteer_referral_codes(
                referral_code, created_by, created_at, is_active, max_uses
            ) VALUES(?, ?, ?, 1, 1)
        """
        cursor.execute(query, (code, created_by, datetime.datetime.now()))
        cnxn.commit()
        return code
    except Exception as e:
        print(f"Error generating code: {e}")
        cnxn.rollback()
        return None
    finally:
        cursor.close()
        cnxn.close()


# Add these NEW functions at the end

def get_referral_codes_by_creator(created_by):
    """Get all referral codes created by a volunteer"""
    cursor, cnxn = get_connection()
    codes_list = []
    try:
        query = """
            SELECT id, referral_code, created_at, is_active, 
                   times_used, max_uses 
            FROM volunteer_referral_codes 
            WHERE created_by=?
            ORDER BY created_at DESC
        """
        cursor.execute(query, (created_by,))
        rows = cursor.fetchall()
        
        for row in rows:
            code_dict = {
                'id': row.id,
                'code': row.referral_code,
                'created_at': row.created_at.isoformat() if row.created_at else None,
                'is_active': row.is_active,
                'times_used': row.times_used,
                'max_uses': row.max_uses,
                'available': row.is_active and row.times_used < row.max_uses
            }
            codes_list.append(code_dict)
    except Exception as e:
        print(f"Error getting codes: {e}")
    finally:
        cursor.close()
        cnxn.close()
    return codes_list

def deactivate_referral_code(code):
    """Deactivate a referral code"""
    cursor, cnxn = get_connection()
    try:
        query = """
            UPDATE volunteer_referral_codes 
            SET is_active = 0 
            WHERE referral_code=?
        """
        cursor.execute(query, (code,))
        cnxn.commit()
        return True
    except Exception as e:
        print(f"Error deactivating code: {e}")
        cnxn.rollback()
        return False
    finally:
        cursor.close()
        cnxn.close()
def count_volunteers():
    """Count how many volunteers exist in system"""
    cursor, cnxn = get_connection()
    try:
        query = "SELECT COUNT(*) FROM user_login WHERE user_type='volunteer'"
        cursor.execute(query)
        result = cursor.fetchone()
        count = result[0] if result else 0
        return count
    except Exception as e:
        print(f"Error counting volunteers: {e}")
        return 0
    finally:
        cursor.close()
        cnxn.close()

# ✅ Get all expenses with documents joined
def get_all_expenses_with_documents():
    """Get expenses with linked documents"""
    cursor, cnxn = get_connection()
    expenses_list = []
    
    try:
        query = """
            SELECT 
                e.id as expense_id,
                e.voucher_number,
                e.amount,
                e.mode_of_payment,
                e.remark_expenses,
                e.created_at,
                e.student_id,
                s.first_name,
                s.last_name,
                d.id as document_id,
                d.document_source_path,
                d.document_source_type
            FROM expenses e
            JOIN students s ON e.student_id = s.id
            LEFT JOIN expense_documents ed ON e.id = ed.expense_id
            LEFT JOIN documents d ON ed.document_id = d.id
            WHERE e.is_active = 1 AND s.is_active = 1
            ORDER BY e.created_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            expense = {
                'expense_id': row.expense_id,
                'voucher_number': row.voucher_number,
                'student_id': row.student_id,
                'first_name': row.first_name,
                'last_name': row.last_name,
                'amount': float(row.amount) if row.amount else 0,
                'mode_of_payment': row.mode_of_payment,
                'remark': row.remark_expenses,
                'date': row.created_at.isoformat() if row.created_at else None,
                'document_id': row.document_id,
                'document_path': row.document_source_path,
                'document_type': row.document_source_type
            }
            expenses_list.append(expense)
    
    except Exception as e:
        print(f"Error fetching expenses: {e}")
    finally:
        cursor.close()
        cnxn.close()
    
    return expenses_list

# ✅ Get student total expenses
def get_student_total_expenses(student_id):
    """Get total expenses for a student"""
    cursor, cnxn = get_connection()
    
    try:
        query = """
            SELECT 
                s.first_name,
                s.last_name,
                COUNT(e.id) as total_payments,
                SUM(e.amount) as total_amount,
                MAX(e.created_at) as last_payment_date
            FROM expenses e
            JOIN students s ON e.student_id = s.id
            WHERE e.student_id = ? AND e.is_active = 1
            GROUP BY s.first_name, s.last_name
        """
        cursor.execute(query, (student_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'first_name': row.first_name,
                'last_name': row.last_name,
                'total_payments': row.total_payments,
                'total_amount': float(row.total_amount) if row.total_amount else 0,
                'last_payment_date': row.last_payment_date.isoformat() if row.last_payment_date else None
            }
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        cnxn.close()

# ✅ Get student expenses with documents
def get_student_expenses_detail(student_id):
    """Get detailed expenses for a student with documents"""
    cursor, cnxn = get_connection()
    expenses = []
    
    try:
        query = """
            SELECT 
                e.id as expense_id,
                e.voucher_number,
                e.amount,
                e.mode_of_payment,
                e.remark_expenses,
                e.created_at,
                d.id as document_id,
                d.document_source_path,
                d.document_source_type
            FROM expenses e
            LEFT JOIN expense_documents ed ON e.id = ed.expense_id
            LEFT JOIN documents d ON ed.document_id = d.id
            WHERE e.student_id = ? AND e.is_active = 1
            ORDER BY e.created_at DESC
        """
        cursor.execute(query, (student_id,))
        rows = cursor.fetchall()
        
        for row in rows:
            expense = {
                'expense_id': row.expense_id,
                'voucher_number': row.voucher_number,
                'amount': float(row.amount) if row.amount else 0,
                'mode_of_payment': row.mode_of_payment,
                'remark': row.remark_expenses,
                'date': row.created_at.isoformat() if row.created_at else None,
                'document_id': row.document_id,
                'document_path': row.document_source_path,
                'document_type': row.document_source_type
            }
            expenses.append(expense)
    
    except Exception as e:
        print(f"Error fetching student expenses: {e}")
    finally:
        cursor.close()
        cnxn.close()
    
    return expenses

# ✅ Get expense summary by payment mode
def get_expenses_by_mode():
    """Get expenses grouped by mode of payment"""
    cursor, cnxn = get_connection()
    summary = {}
    
    try:
        query = """
            SELECT 
                mode_of_payment,
                COUNT(id) as count,
                SUM(amount) as total
            FROM expenses
            WHERE is_active = 1
            GROUP BY mode_of_payment
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            summary[row.mode_of_payment] = {
                'count': row.count,
                'total': float(row.total) if row.total else 0
            }
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        cnxn.close()
    
    return summary