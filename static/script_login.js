const CONFIG = {
  API_LOGIN:    'login_user',
  API_REGISTER: 'register_user',
  DASHBOARD:    'dashboard',
  LOGIN_PAGE:   window.location.href,
};
 
if (sessionStorage.getItem('foch_logged_in') === 'true') {
  window.location.replace(CONFIG.DASHBOARD);
}
 
function switchTab(tab) {
  const isLogin = tab === 'login';
  document.getElementById('tab-login').classList.toggle('active', isLogin);
  document.getElementById('tab-register').classList.toggle('active', !isLogin);
  document.getElementById('pill').classList.toggle('right', !isLogin);
  document.getElementById('panel-login').classList.toggle('active', isLogin);
  document.getElementById('panel-register').classList.toggle('active', !isLogin);
 
  if (isLogin) {
    document.getElementById('left-tagline').innerHTML = 'Write.<br/><em>Create.</em><br/>Belong.';
    document.getElementById('left-sub').innerHTML =
      'A space for those who think in ink.<br/>Credentials hashed, salted,<br/>stored with purpose.';
    document.getElementById('left-foot-txt').textContent = 'Django API · /api/auth/login/';
  } else {
    document.getElementById('left-tagline').innerHTML = 'Join the<br/><em>circle.</em>';
    document.getElementById('left-sub').innerHTML =
      'Your password is hashed with PBKDF2,<br/>salted by Django automatically,<br/>stored in user_login.';
    document.getElementById('left-foot-txt').textContent = 'Django API · /api/auth/register/';
  }
  resetAll();
}
 
async function handleLogin() {
  const username = document.getElementById('l-user').value.trim();
  const password = document.getElementById('l-pass').value;
 
  clearMsg('login-msg');
  setErr('l-user', false); setErr('l-pass', false);
 
  if (!username) { setErr('l-user', true); showMsg('login-msg', 'Username is required.', 'error'); doShake('panel-login'); return; }
  if (!password) { setErr('l-pass', true); showMsg('login-msg', 'Password is required.',  'error'); doShake('panel-login'); return; }
 
  setLoad('btn-login', true);
 
  try {
    const { ok, data } = await post(CONFIG.API_LOGIN, { username, password });
 
    if (ok && data.success) {
      sessionStorage.setItem('foch_logged_in',  'true');
      sessionStorage.setItem('foch_username',    data.username);
      sessionStorage.setItem('foch_last_login',  data.last_login || '');
      showMsg('login-msg', data.message || 'Login successful! Redirecting…', 'success');
      setTimeout(() => window.location.href = CONFIG.DASHBOARD, 700);
    } else {
      showMsg('login-msg', data.error || 'Invalid username or password.', 'error');
      setErr('l-user', true); setErr('l-pass', true);
      doShake('panel-login');
    }
  } catch {
    showMsg('login-msg', 'Cannot reach server. Is Django running?', 'error');
    doShake('panel-login');
  } finally {
    setLoad('btn-login', false);
  }
}
 
async function handleRegister() {
  const username = document.getElementById('r-user').value.trim();
  const password = document.getElementById('r-pass').value;
  const confirm  = document.getElementById('r-cf').value;
 
  clearMsg('reg-msg');
  ['r-user','r-pass','r-cf'].forEach(id => setErr(id, false));
 
  if (!username)           { setErr('r-user', true); showMsg('reg-msg', 'Username is required.', 'error');                     doShake('panel-register'); return; }
  if (username.length < 3) { setErr('r-user', true); showMsg('reg-msg', 'Username must be at least 3 characters.', 'error');  doShake('panel-register'); return; }
  if (!password)           { setErr('r-pass', true); showMsg('reg-msg', 'Password is required.', 'error');                    doShake('panel-register'); return; }
  if (password.length < 4) { setErr('r-pass', true); showMsg('reg-msg', 'Password must be at least 4 characters.', 'error'); doShake('panel-register'); return; }
  if (password !== confirm) { setErr('r-cf', true);  showMsg('reg-msg', 'Passwords do not match.', 'error');                  doShake('panel-register'); return; }
 
  setLoad('btn-reg', true);
 
  try {
    const { ok, data } = await post(CONFIG.API_REGISTER, { username, password });
 
    if (ok && data.success) {
      showMsg('reg-msg', data.message + ' Redirecting to sign in…', 'success');
      setTimeout(() => window.location.href = CONFIG.LOGIN_PAGE, 1500);
    } else {
      showMsg('reg-msg', data.error || 'Registration failed.', 'error');
      const e = (data.error || '').toLowerCase();
      if (e.includes('username')) setErr('r-user', true);
      if (e.includes('password')) setErr('r-pass', true);
      doShake('panel-register');
    }
  } catch {
    showMsg('reg-msg', 'Cannot reach server. Is Django running?', 'error');
    doShake('panel-register');
  } finally {
    setLoad('btn-reg', false);
  }
}
 
function onStrength() {
  const pw = document.getElementById('r-pass').value;
  const sc = calcStrength(pw);
  const CL = ['','w','w','m','s'];
  const LB = ['','Weak','Fair','Good','Strong'];
  for (let i = 1; i <= 4; i++) {
    document.getElementById('s'+i).className = 'seg' + (i <= sc ? ' '+CL[sc] : '');
  }
  document.getElementById('stxt').textContent = pw.length ? LB[sc]+' password' : '';
  onConfirm();
  clearMsg('reg-msg');
}
 
function calcStrength(pw) {
  let s = 0;
  if (pw.length >= 4) s++;
  if (pw.length >= 8) s++;
  if (/[A-Z]/.test(pw) && /[0-9]/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
}
 
function onConfirm() {
  const pw  = document.getElementById('r-pass').value;
  const cf  = document.getElementById('r-cf').value;
  const inp = document.getElementById('r-cf');
  inp.classList.remove('ok','err');
  if (cf) inp.classList.add(pw === cf ? 'ok' : 'err');
}
 
function toggleEye(inputId, iconId) {
  const inp  = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  const show = (inp.type === 'password');
  inp.type = show ? 'text' : 'password';
  icon.innerHTML = show
    ? `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
       <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
       <line x1="1" y1="1" x2="23" y2="23"/>`
    : `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
       <circle cx="12" cy="12" r="3"/>`;
}
 
async function post(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return { ok: res.ok, status: res.status, data: await res.json() };
}
 
function showMsg(id, text, type) {
  const el = document.getElementById(id);
  el.textContent = text;
  el.className = 'msg ' + type;
}
 
function clearMsg(id) {
  const el = document.getElementById(id);
  el.textContent = ''; el.className = 'msg';
}
 
function setErr(id, on) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle('err', on);
  if (on) el.classList.remove('ok');
}
 
function doShake(id) {
  const el = document.getElementById(id);
  el.classList.remove('shake');
  void el.offsetWidth;
  el.classList.add('shake');
  setTimeout(() => el.classList.remove('shake'), 400);
}
 
function setLoad(id, on) {
  const btn = document.getElementById(id);
  btn.disabled = on;
  btn.classList.toggle('loading', on);
}
 
function resetAll() {
  ['l-user','l-pass','r-user','r-pass','r-cf'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.value = '';
    el.classList.remove('err','ok');
  });
  clearMsg('login-msg'); clearMsg('reg-msg');
  for (let i=1;i<=4;i++) document.getElementById('s'+i).className='seg';
  document.getElementById('stxt').textContent = '';
}
 
document.addEventListener('keydown', e => {
  if (e.key !== 'Enter') return;
  document.getElementById('panel-login').classList.contains('active')
    ? handleLogin() : handleRegister();
});
 
document.addEventListener('DOMContentLoaded', () => {
  const map = { 'l-user':'login-msg','l-pass':'login-msg',
                'r-user':'reg-msg','r-pass':'reg-msg','r-cf':'reg-msg' };
  Object.entries(map).forEach(([inputId, msgId]) => {
    document.getElementById(inputId)?.addEventListener('input', () => {
      setErr(inputId, false); clearMsg(msgId);
    });
  });
});