
        // Student data array - will be populated from backend
        let students = [];

        // Function to fetch students from backend
        async function fetchStudents() {
            try {
                const response = await fetch('/api/students', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch students');
                }

                const data = await response.json();
                students = data; // Assuming backend returns array of students
                
                // If backend returns data in a nested structure, adjust accordingly:
                // students = data.students; // or data.data, etc.
                
                console.log('Students fetched:', students);
                renderStudents();
            } catch (error) {
                console.error('Error fetching students:', error);
                alert('Error loading student data. Loading sample data for testing.');
                
                // Fallback to sample data for testing if backend is not ready
                loadSampleData();
            }
        }

        // Sample data fallback for testing without backend
        function loadSampleData() {
            console.log('Loading sample data (backend not available)');
            students = [
                {
                    id: 1,
                    first_name: "Rahul",
                    last_name: "Sharma",
                    date_of_birth: "2005-05-15",
                    gender: "Male",
                    father_name: "Rajesh Sharma",
                    mother_name: "Priya Sharma",
                    parent_contact_number: "9876543210",
                    student_contact_number: "9876543211",
                    address: "123 MG Road, Bangalore",
                    address_location: "Near City Mall, Bangalore",
                    course_pursing: "B.Tech CSE",
                    family_source_of_income: "Business",
                    family_monthly_income: 50000,
                    residential_status: "Own House",
                    additional_assets: "Car, Land",
                    total_monthly_average_expense_siblings: 15000,
                    family_member_count: 4,
                    date_of_joining: "2024-01-15",
                    support_type: "Partial",
                    studying_at: "ABC Engineering College",
                    is_active: true
                },
                {
                    id: 2,
                    first_name: "Priya",
                    last_name: "Patel",
                    date_of_birth: "2006-03-20",
                    gender: "Female",
                    father_name: "Suresh Patel",
                    mother_name: "Meena Patel",
                    parent_contact_number: "9876543212",
                    student_contact_number: "9876543213",
                    address: "456 Brigade Road, Bangalore",
                    address_location: "Near Metro Station, Bangalore",
                    course_pursing: "BCA",
                    family_source_of_income: "Service",
                    family_monthly_income: 40000,
                    residential_status: "Rented",
                    additional_assets: "None",
                    total_monthly_average_expense_siblings: 12000,
                    family_member_count: 5,
                    date_of_joining: "2024-02-01",
                    support_type: "Full",
                    studying_at: "XYZ College",
                    is_active: true
                },
                {
                    id: 3,
                    first_name: "Amit",
                    last_name: "Kumar",
                    date_of_birth: "2005-08-10",
                    gender: "Male",
                    father_name: "Vijay Kumar",
                    mother_name: "Sunita Kumar",
                    parent_contact_number: "9876543214",
                    student_contact_number: "9876543215",
                    address: "789 Whitefield, Bangalore",
                    address_location: "Tech Park Area, Bangalore",
                    course_pursing: "B.Sc IT",
                    family_source_of_income: "Agriculture",
                    family_monthly_income: 30000,
                    residential_status: "Own House",
                    additional_assets: "Agricultural Land",
                    total_monthly_average_expense_siblings: 10000,
                    family_member_count: 6,
                    date_of_joining: "2024-01-20",
                    support_type: "Full",
                    studying_at: "DEF University",
                    is_active: true
                },
                {
                    id: 4,
                    first_name: "Sneha",
                    last_name: "Singh",
                    date_of_birth: "2006-11-25",
                    gender: "Female",
                    father_name: "Arun Singh",
                    mother_name: "Kavita Singh",
                    parent_contact_number: "9876543216",
                    student_contact_number: "9876543217",
                    address: "321 Indiranagar, Bangalore",
                    address_location: "Near 100 Feet Road, Bangalore",
                    course_pursing: "B.Com",
                    family_source_of_income: "Business",
                    family_monthly_income: 60000,
                    residential_status: "Own House",
                    additional_assets: "Shop, Car",
                    total_monthly_average_expense_siblings: 18000,
                    family_member_count: 4,
                    date_of_joining: "2024-03-01",
                    support_type: "Partial",
                    studying_at: "Commerce College",
                    is_active: true
                }
            ];
            renderStudents();
        }

        // Function to create student card element using DOM manipulation
        function createStudentCard(student) {
            // Create card div
            const card = document.createElement('div');
            card.className = 'student-card';

            // Create student header div
            const headerDiv = document.createElement('div');
            headerDiv.className = 'student-header';

            // Create and append student name
            const nameHeading = document.createElement('h3');
            nameHeading.textContent = `${student.first_name} ${student.last_name || ''}`;
            headerDiv.appendChild(nameHeading);

            // Create and append student ID
            const idPara = document.createElement('p');
            idPara.innerHTML = `<strong>ID:</strong> ${student.id}`;
            headerDiv.appendChild(idPara);

            // Create and append course
            const coursePara = document.createElement('p');
            coursePara.innerHTML = `<strong>Course:</strong> ${student.course_pursing}`;
            headerDiv.appendChild(coursePara);

            // Create and append college/institution
            const collegePara = document.createElement('p');
            collegePara.innerHTML = `<strong>College:</strong> ${student.studying_at || 'N/A'}`;
            headerDiv.appendChild(collegePara);

            // Create button group
            const buttonGroup = document.createElement('div');
            buttonGroup.className = 'button-group';

            // Create View button
            const viewBtn = document.createElement('button');
            viewBtn.className = 'btn view-btn';
            viewBtn.textContent = 'View';
            viewBtn.onclick = function() {
                openModal(student, false);
            };

            // Create Manage Expenses button
            const expenseBtn = document.createElement('button');
            expenseBtn.className = 'btn expense-btn';
            expenseBtn.textContent = 'Manage Expenses';
            expenseBtn.onclick = function() {
                openExpenseModal(student);
            };

            // Append buttons to button group
            buttonGroup.appendChild(viewBtn);
            buttonGroup.appendChild(expenseBtn);

            // Append everything to card
            card.appendChild(headerDiv);
            card.appendChild(buttonGroup);

            return card;
        }

        // Function to render all students
        function renderStudents() {
            const container = document.getElementById('studentRecordsContainer');
            
            // Clear existing content
            container.innerHTML = '';

            // Add each student card using DOM manipulation
            students.forEach(student => {
                const studentCard = createStudentCard(student);
                container.appendChild(studentCard);
            });
        }

        // Function to open modal with student details
        function openModal(student, editMode = false) {
            console.log('Opening modal for student:', {
                id: student.id,
                name: `${student.first_name} ${student.last_name}`,
                mode: editMode ? 'EDIT' : 'VIEW'
            });

            const modal = document.getElementById('studentModal');
            const form = document.getElementById('studentForm');
            const modalTitle = document.getElementById('modalTitle');

            // Set modal title
            modalTitle.textContent = editMode ? 'Edit Student Details' : 'Student Details';

            // Clear existing form content
            form.innerHTML = '';

            // Personal Information Section
            const personalSection = createFormSection('Personal Information', [
                { label: 'First Name', name: 'first_name', value: student.first_name, type: 'text' },
                { label: 'Last Name', name: 'last_name', value: student.last_name || '', type: 'text' },
                { label: 'Date of Birth', name: 'date_of_birth', value: student.date_of_birth.split('T')[0], type: 'date' },
                { label: 'Gender', name: 'gender', value: student.gender, type: 'select', options: ['Male', 'Female', 'Other'] },
                { label: 'Is Active?', name: 'is_active', value: student.is_active ? 'Yes' : 'No', type: 'select', options: ['Yes', 'No'] },
                { label: 'Is Delete?', name: 'is_delete', value: student.is_active ? 'No' : 'Yes', type: 'select', options: ['Yes', 'No'] }
            ], editMode);
            form.appendChild(personalSection);

            // Contact Information Section
            const contactSection = createFormSection('Contact Information', [
                { label: "Father's Name", name: 'father_name', value: student.father_name || '', type: 'text' },
                { label: "Mother's Name", name: 'mother_name', value: student.mother_name || '', type: 'text' },
                { label: 'Parent Contact', name: 'parent_contact_number', value: student.parent_contact_number, type: 'tel' },
                { label: 'Student Contact', name: 'student_contact_number', value: student.student_contact_number || '', type: 'tel' },
                { label: 'Address', name: 'address', value: student.address, type: 'textarea', fullWidth: true },
                { label: 'Address Location', name: 'address_location', value: student.address_location || '', type: 'textarea', fullWidth: true }
            ], editMode);
            form.appendChild(contactSection);

            // Academic Information Section
            const academicSection = createFormSection('Academic Information', [
                { label: 'Course Pursuing', name: 'course_pursing', value: student.course_pursing, type: 'text' },
                { label: 'Source of Income', name: 'family_source_of_income', value: student.family_source_of_income, type: 'text' },
                { label: 'Monthly Income', name: 'family_monthly_income', value: student.family_monthly_income, type: 'number' },
                { label: 'Residential Status', name: 'residential_status', value: student.residential_status, type: 'text' },
                { label: 'Additional Assets', name: 'additional_assets', value: student.additional_assets, type: 'text' },
                { label: 'Total Monthly Avg', name: 'total_monthly_average_expense_siblings', value: student.total_monthly_average_expense_siblings, type: 'number' },
                { label: 'Family Members', name: 'family_member_count', value: student.family_member_count, type: 'number' },
                { label: 'Date of Joining', name: 'date_of_joining', value: student.date_of_joining ? student.date_of_joining.split('T')[0] : '', type: 'date' },
                { label: 'Support Type', name: 'support_type', value: student.support_type || '', type: 'text' },
                { label: 'Studying At', name: 'studying_at', value: student.studying_at || '', type: 'text' }
            ], editMode);
            form.appendChild(academicSection);

            // Create footer with buttons
            const footer = document.createElement('div');
            footer.className = 'modal-footer';

            if (editMode) {
                // In edit mode, show Save Changes button
                const saveBtn = document.createElement('button');
                saveBtn.type = 'button';
                saveBtn.className = 'modal-btn save-btn';
                saveBtn.textContent = 'Save Changes';
                saveBtn.onclick = function() {
                    saveStudentChanges(student.id);
                };
                footer.appendChild(saveBtn);
            } else {
                // In view mode, show Edit button
                const editModeBtn = document.createElement('button');
                editModeBtn.type = 'button';
                editModeBtn.className = 'modal-btn edit-mode-btn';
                editModeBtn.textContent = 'Edit';
                editModeBtn.onclick = function() {
                    closeModal();
                    openModal(student, true);
                };
                footer.appendChild(editModeBtn);
            }

            const cancelBtn = document.createElement('button');
            cancelBtn.type = 'button';
            cancelBtn.className = 'modal-btn cancel-btn';
            cancelBtn.textContent = 'Cancel';
            cancelBtn.onclick = closeModal;
            footer.appendChild(cancelBtn);

            form.appendChild(footer);

            // Show modal
            modal.classList.add('show');
        }

        // Function to create form section
        function createFormSection(title, fields, editMode) {
            const section = document.createElement('div');
            section.className = 'form-section';

            const heading = document.createElement('h3');
            heading.textContent = title;
            section.appendChild(heading);

            const row = document.createElement('div');
            row.className = 'form-row';

            fields.forEach(field => {
                const formGroup = document.createElement('div');
                formGroup.className = field.fullWidth ? 'form-group full-width' : 'form-group';

                const label = document.createElement('label');
                label.textContent = field.label;
                formGroup.appendChild(label);

                let input;
                if (field.type === 'select') {
                    input = document.createElement('select');
                    input.name = field.name;
                    field.options.forEach(option => {
                        const opt = document.createElement('option');
                        opt.value = option;
                        opt.textContent = option;
                        opt.selected = option === field.value;
                        input.appendChild(opt);
                    });
                } else if (field.type === 'textarea') {
                    input = document.createElement('textarea');
                    input.name = field.name;
                    input.value = field.value;
                } else {
                    input = document.createElement('input');
                    input.type = field.type;
                    input.name = field.name;
                    input.value = field.value;
                }

                input.disabled = !editMode;
                formGroup.appendChild(input);
                row.appendChild(formGroup);
            });

            section.appendChild(row);
            return section;
        }

        // Function to close modal
        function closeModal() {
            const modal = document.getElementById('studentModal');
            modal.classList.remove('show');
        }

        // Function to save student changes
        function saveStudentChanges(studentId) {
            const form = document.getElementById('studentForm');
            const formData = new FormData(form);
            
            // Prepare properly formatted JSON data for backend
            const updatedData = {
                id: studentId,
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name'),
                date_of_birth: formData.get('date_of_birth'),
                gender: formData.get('gender'),
                is_active: formData.get('is_active') === 'Yes',
                is_delete: formData.get('is_delete') === 'Yes',
                father_name: formData.get('father_name'),
                mother_name: formData.get('mother_name'),
                parent_contact_number: formData.get('parent_contact_number'),
                student_contact_number: formData.get('student_contact_number'),
                address: formData.get('address'),
                address_location: formData.get('address_location'),
                course_pursing: formData.get('course_pursing'),
                family_source_of_income: formData.get('family_source_of_income'),
                family_monthly_income: parseFloat(formData.get('family_monthly_income')),
                residential_status: formData.get('residential_status'),
                additional_assets: formData.get('additional_assets'),
                total_monthly_average_expense_siblings: parseFloat(formData.get('total_monthly_average_expense_siblings')),
                family_member_count: parseInt(formData.get('family_member_count')),
                date_of_joining: formData.get('date_of_joining'),
                support_type: formData.get('support_type'),
                studying_at: formData.get('studying_at'),
                updated_at: new Date().toISOString(),
                updated_by: 'current_user' // Replace with actual logged-in user
            };

            // Log the data
            console.log('Saving student ID:', studentId);
            console.log('Updated data to be sent:', updatedData);
            console.log('JSON Format:', JSON.stringify(updatedData, null, 2));

            // Send to backend API
            fetch(`/update_student/${studentId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                alert('Student updated successfully!');
                closeModal();
                // Refresh the student list from backend
                fetchStudents();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating student. Please check console for details.');
            });

            // Uncomment below and comment out the fetch above for testing without backend
            /*
            alert(`Student Data (JSON):\n\n${JSON.stringify(updatedData, null, 2)}\n\nThis will be sent to: PUT /api/students/${studentId}\n\nCheck console for full data.`);
            closeModal();
            */
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('studentModal');
            const expenseModal = document.getElementById('expenseModal');
            if (event.target === modal) {
                closeModal();
            }
            if (event.target === expenseModal) {
                closeExpenseModal();
            }
        }

        // Global variable to store current student for expense
        let currentExpenseStudent = null;

        // Function to open expense modal
        function openExpenseModal(student) {
            currentExpenseStudent = student;
            console.log('Opening expense modal for student:', {
                id: student.id,
                name: `${student.first_name} ${student.last_name}`
            });

            const modal = document.getElementById('expenseModal');
            const title = document.getElementById('expenseModalTitle');
            
            // Update title with student name
            title.textContent = `Manage Expenses - ${student.first_name} ${student.last_name || ''}`;
            
            // Reset form
            document.getElementById('expenseForm').reset();
            
            // Show modal
            modal.classList.add('show');
        }

        // Function to close expense modal
        function closeExpenseModal() {
            const modal = document.getElementById('expenseModal');
            modal.classList.remove('show');
            currentExpenseStudent = null;
        }

        // Function to preview expense receipt
        function previewExpenseReceipt(event) {
            const file = event.target.files[0];
            const preview = document.getElementById('receiptPreview');
            
            if (!file) {
                preview.innerHTML = '';
                preview.classList.remove('show');
                return;
            }
            
            // Validate file type
            const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
            if (!validTypes.includes(file.type)) {
                alert('Please select a JPG, PNG, or PDF file');
                event.target.value = '';
                preview.innerHTML = '';
                preview.classList.remove('show');
                return;
            }
            
            // Validate file size (5MB)
            if (file.size > 5 * 1024 * 1024) {
                alert('File must be less than 5MB');
                event.target.value = '';
                preview.innerHTML = '';
                preview.classList.remove('show');
                return;
            }
            
            preview.classList.add('show');
            
            // Show preview based on file type
            if (file.type === 'application/pdf') {
                preview.innerHTML = `
                    <div class="pdf-icon">📄 PDF Receipt</div>
                    <div class="file-info">
                        ${file.name} (${(file.size / 1024).toFixed(2)} KB)
                    </div>
                `;
            } else {
                // Image preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.innerHTML = `
                        <img src="${e.target.result}" alt="Receipt Preview">
                        <div class="file-info">
                            ${file.name} (${(file.size / 1024).toFixed(2)} KB)
                        </div>
                    `;
                };
                reader.readAsDataURL(file);
            }
        }
 
        /* REMOVED: Remove file button - User can simply click "Choose File" again to change
        function removeReceiptFile() {
            const fileInput = document.getElementById('expenseReceipt');
            const preview = document.getElementById('receiptPreview');
            
            fileInput.value = '';
            preview.innerHTML = '';
            preview.classList.remove('show');
        }
        */
 
        // Function to save expense
        async function saveExpense() {
            const form = document.getElementById('expenseForm');
            
            // Validate form
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            
            const formData = new FormData(form);
            const fileInput = document.getElementById('expenseReceipt');
            
            // Prepare JSON data for backend with student_id from the specific card clicked
            const expenseData = {
                student_id: currentExpenseStudent.id,  // Student ID from the clicked card
                amount: parseFloat(formData.get('amount')),
                mode_of_payment: formData.get('mode_of_payment'),
                remark: formData.get('remark') || '',
                //created_at: new Date().toISOString(),
                //created_by: 'current_user' // Replace with actual logged-in user
            };
 
            // Log the data clearly
            console.log('===== EXPENSE DATA TO SEND =====');
            console.log('Student ID:', expenseData.student_id);
            console.log('Student Name:', `${currentExpenseStudent.first_name} ${currentExpenseStudent.last_name}`);
            console.log('Full JSON:', JSON.stringify(expenseData, null, 2));
            console.log('Has Receipt File:', fileInput.files.length > 0);
            console.log('================================');
 
            try {
                // Step 1: Save expense data to backend
                const response = await fetch('/expenses', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(expenseData)
                });
 
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
 
                const result = await response.json();
                console.log('Backend Response:', result);
                
                const expenseId = result.expense_id; // Backend should return the created expense ID
                
                // Step 2: Upload receipt file if selected
                if (fileInput.files.length > 0) {
                    const uploadFormData = new FormData();
                    uploadFormData.append('receipt', fileInput.files[0]);
                    uploadFormData.append('student_id', currentExpenseStudent.id);
                    uploadFormData.append('expense_id', expenseId);
                    
                    const uploadResponse = await fetch(`/upload_expense/${expenseId}`, {
                        method: 'POST',
                        body: uploadFormData
                    });
                    
                    if (!uploadResponse.ok) {
                        console.warn('Receipt upload failed, but expense was saved');
                    } else {
                        const uploadResult = await uploadResponse.json();
                        console.log('Receipt uploaded:', uploadResult.file_path);
                    }
                }
                
                alert(`Expense saved successfully for ${currentExpenseStudent.first_name} ${currentExpenseStudent.last_name}!`);
                closeExpenseModal();
                
            } catch (error) {
                console.error('Error:', error);
                alert('Error saving expense. Please check console for details.');
            }
 
            // Uncomment below and comment out the fetch above for testing without backend
            /*
            let message = `Expense Data (JSON):\n\n${JSON.stringify(expenseData, null, 2)}\n\nStudent: ${currentExpenseStudent.first_name} ${currentExpenseStudent.last_name}\nStudent ID: ${expenseData.student_id}`;
            
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                message += `\n\nReceipt File:\n- Name: ${file.name}\n- Size: ${(file.size / 1024).toFixed(2)} KB\n- Type: ${file.type}`;
            }
            
            message += '\n\nThis will be sent to: POST /api/expenses';
            alert(message);
            closeExpenseModal();
            */
        }
 
        // Initialize - Fetch students from backend when page loads
        document.addEventListener('DOMContentLoaded', function() {
            fetchStudents();
        });
 
        // Optional: Function to add new student dynamically
        function addStudent(studentData) {
            students.push(studentData);
            renderStudents();
        }
 
        // Optional: Function to remove student
        function removeStudent(studentId) {
            const index = students.findIndex(s => s.id === studentId);
            if (index > -1) {
                students.splice(index, 1);
                renderStudents();
            }
        }