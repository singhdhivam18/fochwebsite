/* =========================================
   1. GLOBAL CONFIG
   ========================================= */
   const API_BASE_URL = "http://127.0.0.1:8000";

   /* =========================================
      2. DASHBOARD LOGIC 
      (Triggered by /dashboard)
      ========================================= */
   async function loadDashboard() {
       const statsContainer = document.getElementById("totalStudents");
       if (!statsContainer) return; // Exit if not on Dashboard page
   
       try {
           const response = await fetch(`${API_BASE_URL}/api`);
           const data = await response.json();
   
           document.getElementById("totalStudents").innerText = data.activestudentcount;
           document.getElementById("attendance").innerText = data.averageStudentAttendence + "%";
   
           const birthdayList = document.getElementById("birthdayList");
           birthdayList.innerHTML = "";
           data.upcomingbirthdays.forEach(item => {
               const li = document.createElement("li");
               const date = new Date(item.dateOfbirth).toLocaleDateString("en-GB", { day: "2-digit", month: "short" });
               li.innerText = `${item.firstname} ${item.lastname} - ${date}`;
               birthdayList.appendChild(li);
           });
       } catch (error) {
           console.error("Dashboard API Error:", error);
       }
   }
   
   /* =========================================
      3. STUDENT LIST LOGIC 
      (Triggered by /students-list)
      ========================================= */
   /*async function fetchStudents() {
       const tableBody = document.getElementById("studentTableBody");
       if (!tableBody) return; // Exit if not on Student List page
   
       try {
           // This is the call that happens when you click 'Student Records'
           const response = await fetch(`${API_BASE_URL}/api/students`); 
           const data = await response.json();
   
           tableBody.innerHTML = ""; 
   
           data.forEach(student => {
               const row = document.createElement("tr");
               const statusClass = student.is_active ? "status-active" : "status-inactive";
               
               row.innerHTML = `
                   <td>${student.id}</td>
                   <td>${student.first_name} ${student.last_name}</td>
                   <td>${student.date_of_birth || '-'}</td>
                   <td>${student.gender}</td>
                   <td>${student.father_name || '-'}</td>
                   <td>${student.course_pursing || '-'}</td>
                   <td>${student.support_type || '-'}</td>
                   <td><span class="status-badge ${statusClass}">${student.is_active ? 'Active' : 'Inactive'}</span></td>
               `;
               tableBody.appendChild(row);
           });
       } catch (error) {
           console.error("Table API Error:", error);
           tableBody.innerHTML = "<tr><td colspan='8' style='text-align:center; color:red;'>Error loading student records.</td></tr>";
       }
   }
   */
   /* =========================================
      4. MODAL & FORM LOGIC
      ========================================= */

   const modal = document.getElementById("studentModal");
   
   function openStudentModal() { if(modal) modal.style.display = "block"; }
   function closeStudentModal() { if(modal) modal.style.display = "none"; }
   
   // Handle Form Submission
   const studentForm = document.getElementById("studentForm");
   if (studentForm) {
       studentForm.addEventListener("submit", async function(e) {
           e.preventDefault();
           const formData = new FormData(e.target);
           
           // Match the specific JSON structure your backend expects
           const studentData = Object.fromEntries(formData.entries());
           // Convert types for backend compatibility
           studentData.is_active = studentData.is_active === 'true';
           studentData.family_monthly_income = parseFloat(studentData.family_monthly_income) || 0;
            console.log(studentData)
           try {
               const response = await fetch(`${API_BASE_URL}/insert`, {
                   method: "POST",
                   headers: { "Content-Type": "application/json" },
                   body: JSON.stringify(studentData)
               });
   
               if (response.ok) {
                   alert("Student registered successfully!");
                   closeStudentModal();
                   studentForm.reset();
                   // Refresh data for whichever page is currently active
                   loadDashboard();
                   fetchStudents();
               }
           } catch (error) {
               alert("Submission failed. Check console.");
           }
       });
   }

   
   /* =========================================
      5. INITIALIZE ON PAGE LOAD
      ========================================= */
   document.addEventListener("DOMContentLoaded", () => {
       loadDashboard();
       //fetchStudents();
   });
// Set today's date as default
document.getElementById('attendance-date').valueAsDate = new Date();
// Restrict date picker to Sundays only
const dateInput = document.getElementById('attendance-date');
dateInput.addEventListener('input', function () {
    const selected = new Date(this.value);
    // getDay() returns 0 for Sunday
    if (selected.getDay() !== 0) {
        this.value = '';
        alert('Only Sundays can be selected');
    }
});



// Function to add students dynamically
function addStudent(student) {
    const studentsList = document.getElementById('studentsList');
    
    const studentRow = document.createElement('div');
    studentRow.className = 'student-row';
    
    // FIX: Handle boolean values from backend
    let status = 'present'; // default
    
    if (student.has_attendence === null || student.has_attendence === undefined) {
        status = 'present';
    } else if (student.has_attendence === false || student.has_attendence === 0 || student.has_attendence === 'absent') {
        status = 'absent';
    } else if (student.has_attendence === true || student.has_attendence === 1 || student.has_attendence === 'present') {
        status = 'present';
    }
    
    console.log(`${student.first_name} ${student.last_name} - status: ${status}`);
    
    studentRow.innerHTML = `
        <div class="student-name">${student.first_name} ${student.last_name}</div>
        <div class="attendance-options">
            <div class="radio-option present">
                <input type="radio"
                    id="present-${student.id}"
                    name="attendance-${student.id}"
                    value="present"
                    ${status === 'present' ? 'checked' : ''}>
                <label for="present-${student.id}">Present</label>
            </div>
            <div class="radio-option absent">
                <input type="radio"
                    id="absent-${student.id}"
                    name="attendance-${student.id}"
                    value="absent"
                    ${status === 'absent' ? 'checked' : ''}>
                <label for="absent-${student.id}">Absent</label>
            </div>
        </div>
    `;
    studentsList.appendChild(studentRow);
}
let studentsData = []; // Declare globally
let count = 0;         // Declare globally
// Async function to fetch students from backend
async function loadStudents() {
    try {
        const response = await fetch('getdetails');
        const students = await response.json();
        console.log('Fetched students:', students);

        // Store globally
        studentsData = students;
        count = studentsData.length;
        console.log('Total students:', count);
        console.log('studentsData after load:', studentsData);
        
        // Clear existing list before adding
        const studentsList = document.getElementById('studentsList');
        studentsList.innerHTML = '';
        
        // Add each student to the list
        students.forEach(student => {
            addStudent(student);
        });
        
        console.log('Students rendered. studentsData is now:', studentsData);
        
    } catch (error) {
        console.error('Error loading students:', error);
        alert('Failed to load students. Please try again.');
    }
}
// Async function to submit attendance
async function submitAttendance() {
    const dateInput = document.getElementById('attendance-date');
    const date = dateInput.value;
    
    if (!date) {
        alert('Please select a date');
        return;
    }

    const attendanceData = {
        date: date,
        records: []
    };
    
    // DEBUG: Check what studentsData contains
    console.log('studentsData:', studentsData);
    
    
    // Collect attendance status for each student
    studentsData.forEach(student => {
        const presentRadio = document.getElementById(`present-${student.id}`);
        const absentRadio = document.getElementById(`absent-${student.id}`);
        
        // DEBUG: Log each student's radio button state
        console.log(`Student ${student.id}:`, {
            presentRadio: presentRadio,
            absentRadio: absentRadio,
            presentChecked: presentRadio ? presentRadio.checked : 'not found',
            absentChecked: absentRadio ? absentRadio.checked : 'not found'
        });
        
        let status = null;
        if (presentRadio && presentRadio.checked) {
            status = 'present';
        } else if (absentRadio && absentRadio.checked) {
            status = 'absent';
        }

        console.log(`Student ${student.id} status:`, status);

        // Add to records if status is determined
        if (status) {
            attendanceData.records.push({
                studentId: student.id,
                studentName: student.first_name + ' ' + student.last_name,
                status: status,
                date: date
            });
        }
    });

    console.log('attendanceData.records:', attendanceData.records);
    console.log('records.length:', attendanceData.records.length);

    // Validation
    if (attendanceData.records.length === 0) {
        alert('Please mark attendance for at least one student');
        return;
    }
    
    if (attendanceData.records.length !== count) {
        alert(`Please mark attendance for all students (${attendanceData.records.length}/${count} marked)`);
        return;
    }

    try {
        console.log('Submitting Attendance Data to Backend:');
        console.log(JSON.stringify(attendanceData, null, 2));
        
        const response = await fetch('put_attendance', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(attendanceData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Backend Response:', result);
        
        if (response.status === 202) {
            alert("updated successfully");
        } else {
            alert('Attendance submitted successfully!');
        }
        
    } catch (error) {
        console.error('Error submitting attendance:', error);
        alert('Failed to submit attendance. Please try again.');
    }
}
async function deleteAttendance() {
    const deleteDate = document.getElementById('delete-date').value;
    
    if (!deleteDate) {
        alert('Please select a date');
        return;
    }

    try {
        console.log('Deleting attendance for date:', deleteDate);

        // Use the same URL pattern as your other endpoints
        const response = await fetch('delete_attendance', {  // Changed this line
            method: 'DELETE',  // Or 'DELETE' if your Django view supports it
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date: deleteDate })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Delete response:', result);
        alert('Attendance deleted successfully!');
        
        // Clear the date input
        document.getElementById('delete-date').value = '';
        
    } catch (error) {
        console.error('Error deleting attendance:', error);
        alert('Failed to delete attendance. Please try again.');
    }
}
// Load students when page loads
//loadStudents();

//load attendance
async function loadAttendance() {
    const date = document.getElementById('attendance-date').value;
    const loadBtn = document.getElementById('loadBtn');

    if (!date) {
        console.log('Please select a date');
        return;
    }

    // Validate Sunday again
    const selected = new Date(date);
    if (selected.getDay() !== 0) {
        alert('Only Sundays allowed');
        return;
    }

    loadBtn.disabled = true;
    loadBtn.textContent = 'Loading...';

    try {
        // Check if attendance exists for this date
        const response = await fetch(`check_attendance?date=${date}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Backend Response:', result);
        
        // FIX 1: Use response.status as NUMBER not STRING
        if (response.status === 203) {
            // No attendance exists - load fresh students
            await loadStudents();
            alert("This date data is not present! Loading fresh student list.");
        }
        else if (response.status === 202) {
            // Attendance exists - load existing attendance
            
            // FIX 2: Don't redeclare response/result variables
            const attendanceResponse = await fetch(`get_attendance_exists?date=${date}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            const attendanceResult = await attendanceResponse.json();
            
            // FIX 3: Set studentsData globally, not local 'students'
            studentsData = attendanceResult.students;
            count = studentsData.length;
            
            console.log('✅ studentsData loaded:', studentsData);
            console.log('✅ count:', count);

            // Clear existing list
            const studentsList = document.getElementById('studentsList');
            studentsList.innerHTML = '';

            // Render with already marked data from backend
            studentsData.forEach(student => {
                addStudent(student);
            });
            
            console.log('Loaded attendance for:', date, attendanceResult);
        }
        
    } catch (error) {
        console.error('Error loading attendance:', error);
        alert('Failed to load attendance. Please try again.');
    }

    loadBtn.disabled = false;
    loadBtn.textContent = 'Load';
}

/* ← your login page URL */

async function handleLogout(event) {
    event.preventDefault();
    sessionStorage.removeItem('foch_logged_in');
    sessionStorage.removeItem('foch_username');
    sessionStorage.removeItem('foch_last_login');
    window.location.href = `${API_BASE_URL}/login`;
}