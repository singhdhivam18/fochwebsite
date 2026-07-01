
// ✅ NEW: Handle user type change
function onUserTypeChange() {
  const userType = document.getElementById('r-type').value;
  const referralField = document.getElementById('referral-field');
  
  if (userType === 'volunteer') {
    referralField.style.display = 'block';  // Show referral code field
  } else {
    referralField.style.display = 'none';   // Hide for students
  }
}

// ✅ UPDATED: handleRegister with user_type
function handleRegister() {
  const username = document.getElementById('r-user').value.trim();
  const password = document.getElementById('r-pass').value;
  const confirm = document.getElementById('r-cf').value;
  const userType = document.getElementById('r-type').value;  // NEW
  const referralCode = document.getElementById('r-code').value.trim();  // NEW
  
  const msgBox = document.getElementById('reg-msg');
  const btn = document.getElementById('btn-reg');

  // Validation
  if (!username || !password) {
    msgBox.textContent = '❌ Username and password required';
    msgBox.classList.add('error');
    return;
  }

  if (password !== confirm) {
    msgBox.textContent = '❌ Passwords do not match';
    msgBox.classList.add('error');
    return;
  }

  // For volunteers, check referral code
  if (userType === 'volunteer' && !referralCode) {
    msgBox.textContent = '❌ Referral code required for volunteers';
    msgBox.classList.add('error');
    return;
  }

  // Disable button and show spinner
  btn.disabled = true;
  btn.classList.add('loading');

  // ✅ Send registration with user_type and referral_code
  fetch('/register_user', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: username,
      password: password,
      user_type: userType,        // 🎯 Send user_type
      referral_code: referralCode // 🎯 Send referral code if volunteer
    })
  })
  .then(res => res.json())
  .then(data => {
    btn.disabled = false;
    btn.classList.remove('loading');
    
    if (data.success) {
      msgBox.textContent = `✅ ${data.message}`;
      msgBox.classList.remove('error');
      msgBox.classList.add('success');
      
      // Clear form
      document.getElementById('r-user').value = '';
      document.getElementById('r-pass').value = '';
      document.getElementById('r-cf').value = '';
      document.getElementById('r-code').value = '';
      
      // Redirect after 1.5s
      setTimeout(() => switchTab('login'), 1500);
    } else {
      msgBox.textContent = `❌ ${data.error}`;
      msgBox.classList.add('error');
    }
  })
  .catch(err => {
    btn.disabled = false;
    btn.classList.remove('loading');
    msgBox.textContent = '❌ Network error';
    msgBox.classList.add('error');
    console.error(err);
  });
}

// ✅ UPDATED: handleLogin to store user_type
// ✅ UPDATED: handleLogin to store user_type
function handleLogin() {
  const username = document.getElementById('l-user').value.trim();
  const password = document.getElementById('l-pass').value;
  
  const msgBox = document.getElementById('login-msg');
  const btn = document.getElementById('btn-login');

  if (!username || !password) {
    msgBox.textContent = '❌ Both fields required';
    msgBox.classList.add('error');
    return;
  }

  btn.disabled = true;
  btn.classList.add('loading');

  fetch('/login_user', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: username,
      password: password
    })
  })
  .then(res => res.json())
  .then(data => {
    btn.disabled = false;
    btn.classList.remove('loading');
    
    if (data.success) {
      msgBox.textContent = `✅ ${data.message}`;
      msgBox.classList.remove('error');
      msgBox.classList.add('success');
      
      // 🎯 FIXED: Use sessionStorage with correct key names
      sessionStorage.setItem('foch_user_type', data.user_type);
      sessionStorage.setItem('foch_username', data.username);
      sessionStorage.setItem('foch_logged_in', 'true');
      sessionStorage.setItem('foch_last_login', data.last_login || '');
      
      console.log(`✅ Logged in as ${data.user_type}: ${data.username}`);
      
      // Redirect to dashboard
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 1000);
    } else {
      msgBox.textContent = `❌ ${data.error}`;
      msgBox.classList.add('error');
    }
  })
  .catch(err => {
    btn.disabled = false;
    btn.classList.remove('loading');
    msgBox.textContent = '❌ Network error';
    msgBox.classList.add('error');
    console.error(err);
  });
}

// ✅ Toggle password visibility
function toggleEye(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  
  if (input.type === 'password') {
    input.type = 'text';
    icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/><line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="2"/>';
  } else {
    input.type = 'password';
    icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
  }
}

// ✅ Password strength checker
function onStrength() {
  const pass = document.getElementById('r-pass').value;
  const s1 = document.getElementById('s1');
  const s2 = document.getElementById('s2');
  const s3 = document.getElementById('s3');
  const s4 = document.getElementById('s4');
  const stxt = document.getElementById('stxt');
  
  let strength = 0;
  
  if (pass.length >= 4) strength++;
  if (/[a-z]/.test(pass) && /[A-Z]/.test(pass)) strength++;
  if (/[0-9]/.test(pass)) strength++;
  if (/[^a-zA-Z0-9]/.test(pass)) strength++;
  
  // Reset
  s1.style.backgroundColor = '#ccc';
  s2.style.backgroundColor = '#ccc';
  s3.style.backgroundColor = '#ccc';
  s4.style.backgroundColor = '#ccc';
  
  if (strength >= 1) s1.style.backgroundColor = '#f59e0b';
  if (strength >= 2) s2.style.backgroundColor = '#f59e0b';
  if (strength >= 3) s3.style.backgroundColor = '#10b981';
  if (strength >= 4) s4.style.backgroundColor = '#10b981';
  
  const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
  stxt.textContent = labels[strength];
}

// ✅ Password confirm checker
function onConfirm() {
  const pass = document.getElementById('r-pass').value;
  const conf = document.getElementById('r-cf').value;
  
  if (conf && pass !== conf) {
    document.getElementById('r-cf').style.borderColor = '#ef4444';
  } else {
    document.getElementById('r-cf').style.borderColor = '#d1d5db';
  }
}

// ✅ Tab switching
function switchTab(tab) {
  document.getElementById('panel-login').classList.toggle('active', tab === 'login');
  document.getElementById('panel-register').classList.toggle('active', tab === 'register');
  document.getElementById('tab-login').classList.toggle('active', tab === 'login');
  document.getElementById('tab-register').classList.toggle('active', tab === 'register');
  
  const pill = document.getElementById('pill');
  if (tab === 'login') {
    pill.style.transform = 'translateX(0)';
  } else {
    pill.style.transform = 'translateX(100%)';
  }
}