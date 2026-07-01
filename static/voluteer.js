

// 🎯 Check authentication on page load
const username = sessionStorage.getItem('foch_username');
const userType = sessionStorage.getItem('foch_user_type');

if (!username || userType !== 'volunteer') {
    alert('❌ Unauthorized. Only volunteers can access this page.');
    window.location.href = '/login';
}

// Update user info
document.getElementById('userInfo').textContent = `Welcome, ${username} (Volunteer)`;

// Load codes on page load
window.addEventListener('load', loadCodes);

// ✅ Generate new code
async function generateNewCode() {
    const btn = document.getElementById('genBtn');
    const spinner = document.getElementById('genSpinner');
    const msg = document.getElementById('genMessage');
    
    btn.disabled = true;
    spinner.style.display = 'inline-block';
    
    try {
        const response = await fetch('/api/generate-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(msg, `✅ Code generated: ${data.code}`, 'success');
            console.log('New code:', data.code);
            loadCodes(); // Reload list
        } else {
            showMessage(msg, `❌ ${data.error}`, 'error');
        }
    } catch (err) {
        console.error(err);
        showMessage(msg, '❌ Network error', 'error');
    } finally {
        btn.disabled = false;
        spinner.style.display = 'none';
    }
}

// ✅ Load codes
async function loadCodes() {
    const list = document.getElementById('codeList');
    
    try {
        const response = await fetch(`/api/get-codes?username=${username}`);
        const data = await response.json();
        
        if (data.success && data.codes.length > 0) {
            list.innerHTML = data.codes.map(code => `
                <li class="code-item">
                    <div class="code-info">
                        <div class="code-value">${code.code}</div>
                        <div class="code-meta">
                            Created: ${new Date(code.created_at).toLocaleDateString()}
                            • Used: ${code.times_used}/${code.max_uses}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <span class="code-status ${code.available ? 'status-active' : code.is_active ? 'status-used' : 'status-inactive'}">
                            ${code.available ? '✓ Available' : code.is_active ? '⚠ Used' : '✗ Inactive'}
                        </span>
                        <button class="copy-btn" onclick="copyCode('${code.code}')">📋 Copy</button>
                        ${code.is_active ? `<button class="deactivate-btn" onclick="deactivateCode('${code.code}')">🔒 Deactivate</button>` : ''}
                    </div>
                </li>
            `).join('');
        } else {
            list.innerHTML = `
                <div class="empty-state">
                    <p>No codes generated yet</p>
                    <p style="font-size: 12px; margin-top: 10px;">Click "Generate Code" to create one</p>
                </div>
            `;
        }
    } catch (err) {
        console.error(err);
        list.innerHTML = `<div class="empty-state"><p>❌ Error loading codes</p></div>`;
    }
}

// ✅ Copy code to clipboard
function copyCode(code) {
    navigator.clipboard.writeText(code).then(() => {
        alert(`✅ Copied: ${code}`);
    }).catch(err => {
        console.error('Copy failed:', err);
    });
}

// ✅ Deactivate code
async function deactivateCode(code) {
    if (!confirm(`Deactivate code ${code}?`)) return;
    
    try {
        const response = await fetch('/api/deactivate-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, username: username })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Code deactivated');
            loadCodes();
        } else {
            alert(`❌ ${data.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('❌ Network error');
    }
}

// ✅ Show message
function showMessage(el, text, type) {
    el.textContent = text;
    el.className = `message show ${type}`;
    setTimeout(() => {
        el.classList.remove('show');
    }, 5000);
}

// ✅ Logout
function handleLogout() {
    sessionStorage.clear();
    window.location.href = '/login';
}