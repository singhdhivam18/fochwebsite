
window.addEventListener('load', () => {
    loadExpenses();
    loadPaymentSummary();
});

// Load all expenses
async function loadExpenses() {
    try {
        const response = await fetch('/api/expenses-with-docs');
        const data = await response.json();

        if (data.success && data.expenses.length > 0) {
            displayExpenses(data.expenses);
        } else {
            document.getElementById('emptyState').style.display = 'block';
        }
    } catch (err) {
        console.error('Error:', err);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// Display expenses
function displayExpenses(expenses) {
    const tbody = document.getElementById('expenseTableBody');
    let totalAmount = 0;
    let totalPayments = 0;
    let totalStudents = new Set();
    let withDocs = 0;

    tbody.innerHTML = expenses.map(exp => {
        totalAmount += exp.amount;
        totalPayments++;
        totalStudents.add(exp.student_id);
        if (exp.document_path) withDocs++;

        return `
            <tr>
                <td class="student-name">${exp.first_name} ${exp.last_name}</td>
                <td><span class="badge badge-primary">${exp.voucher_number}</span></td>
                <td class="amount">₹${exp.amount.toFixed(2)}</td>
                <td><span class="badge badge-info">${exp.mode_of_payment}</span></td>
                <td>${new Date(exp.date).toLocaleDateString()}</td>
                <td>${exp.remark || '-'}</td>
                <td>
                    ${exp.document_path ? 
                        `<button class="action-btn action-btn-download" onclick="downloadDocument(${exp.document_id})">📄 Download</button>` 
                        : '<span style="color: #999;">No</span>'}
                </td>
                <td>
                    <button class="action-btn" onclick="viewDetail(${exp.student_id}, '${exp.first_name} ${exp.last_name}')">👁️ View</button>
                </td>
            </tr>
        `;
    }).join('');

    // Update summary
    document.getElementById('totalAmount').textContent = `₹${totalAmount.toFixed(2)}`;
    document.getElementById('totalPayments').textContent = totalPayments;
    document.getElementById('totalStudents').textContent = totalStudents.size;
    document.getElementById('withDocuments').textContent = withDocs;

    document.getElementById('allExpensesTable').style.display = 'block';
}

// Load payment summary
async function loadPaymentSummary() {
    try {
        const response = await fetch('/api/expenses-summary');
        const data = await response.json();

        if (data.success) {
            const summary = data.summary;
            const html = Object.entries(summary).map(([mode, stats]) => `
                <div class="expense-item">
                    <div class="expense-header">
                        <h4>${mode}</h4>
                        <span class="expense-amount">₹${stats.total.toFixed(2)}</span>
                    </div>
                    <div class="expense-details">
                        <div class="detail-row">
                            <span class="detail-label">Payments:</span>
                            <span class="detail-value">${stats.count}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Avg Amount:</span>
                            <span class="detail-value">₹${(stats.total / stats.count).toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            `).join('');

            document.getElementById('paymentSummary').innerHTML = html;
        }
    } catch (err) {
        console.error('Error:', err);
    }
}

// View student detail
async function viewDetail(studentId, studentName) {
    try {
        const response = await fetch(`/api/student-expenses-detail/${studentId}`);
        const data = await response.json();

        if (data.success) {
            const expenses = data.expenses;
            let total = 0;
            const html = expenses.map(exp => {
                total += exp.amount;
                return `
                    <div class="expense-item">
                        <div class="expense-header">
                            <h4>₹${exp.amount.toFixed(2)}</h4>
                            <span class="badge badge-info">${new Date(exp.date).toLocaleDateString()}</span>
                        </div>
                        <div class="expense-details">
                            <div class="detail-row">
                                <span class="detail-label">Voucher:</span>
                                <span class="detail-value">${exp.voucher_number}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Mode:</span>
                                <span class="detail-value">${exp.mode_of_payment}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Remark:</span>
                                <span class="detail-value">${exp.remark || '-'}</span>
                            </div>
                        </div>
                        ${exp.document_path ? `
                            <div class="expense-actions">
                                <button class="action-btn action-btn-download" onclick="downloadDocument(${exp.document_id})">📄 Download Receipt</button>
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('');

            document.getElementById('studentDetailName').textContent = `${studentName} - Total: ₹${total.toFixed(2)}`;
            document.getElementById('detailBody').innerHTML = html;
            document.getElementById('detailModal').style.display = 'block';
        }
    } catch (err) {
        console.error('Error:', err);
    }
}

// Download document
function downloadDocument(docId) {
    window.location.href = `/api/download-document/${docId}`;
}

// Switch tabs
function switchTab(tab) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
    event.target.classList.add('active');
}

// Close modal
function closeDetailModal() {
    document.getElementById('detailModal').style.display = 'none';
}

// Print
function printReport() {
    window.print();
}

// Download CSV
function downloadCSV() {
    const table = document.querySelector('#allExpensesTable table');
    if (!table) return;

    let csv = [];
    table.querySelectorAll('th').forEach(th => {
        csv.push('"' + th.textContent.trim() + '"');
    });
    csv = [csv.join(',')];

    table.querySelectorAll('tbody tr').forEach(tr => {
        const row = [];
        tr.querySelectorAll('td').forEach((td, i) => {
            if (i < 7) row.push('"' + td.textContent.trim() + '"');
        });
        csv.push(row.join(','));
    });

    const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `expense-report-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
}

// Go back
function goBack() {
    window.history.back();
}

// Close modal on outside click
window.onclick = (event) => {
    const modal = document.getElementById('detailModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}