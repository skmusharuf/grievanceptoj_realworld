// Ensure user is logged out
requireLogout();

// DOM Elements
const loginForm = document.getElementById('loginForm');
const errorMessage = document.getElementById('errorMessage');
const loginBtn = document.getElementById('loginBtn');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    
    if (!email || !password) {
        errorMessage.textContent = 'Please enter both email and password';
        errorMessage.style.display = 'block';
        return;
    }
    
    loginBtn.disabled = true;
    loginBtn.textContent = 'Signing in...';
    errorMessage.style.display = 'none';
    
    try {
        const response = await apiCall('/api/auth/admin/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        
        if (response.success) {
            // Save session
            SessionManager.setToken(response.session_token);
            SessionManager.setAdminInfo(response.admin);
            
            console.log('[v0] Login successful, redirecting to dashboard');
            window.location.href = 'admin-dashboard.html';
        }
    } catch (error) {
        errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
        errorMessage.style.display = 'block';
    } finally {
        loginBtn.disabled = false;
        loginBtn.textContent = 'Sign In';
    }
});
