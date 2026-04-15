/**
 * Admin Login Module
 * Handles admin authentication with OTP
 */

/**
 * Initialize admin login
 */
function initializeAdminLogin() {
  setupEmailStep();
  setupOtpStep();
}

/**
 * Setup email step listeners
 */
function setupEmailStep() {
  const sendOtpBtn = document.getElementById('sendOtpBtn');
  const adminEmail = document.getElementById('adminEmail');
  
  if (sendOtpBtn) {
    sendOtpBtn.addEventListener('click', handleSendOtp);
  }
  
  if (adminEmail) {
    adminEmail.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        handleSendOtp();
      }
    });
  }
}

/**
 * Setup OTP step listeners
 */
function setupOtpStep() {
  const verifyOtpBtn = document.getElementById('verifyOtpBtn');
  const backToEmailBtn = document.getElementById('backToEmailBtn');
  const adminOtp = document.getElementById('adminOtp');
  
  if (verifyOtpBtn) {
    verifyOtpBtn.addEventListener('click', handleVerifyOtp);
  }
  
  if (backToEmailBtn) {
    backToEmailBtn.addEventListener('click', showEmailStep);
  }
  
  if (adminOtp) {
    adminOtp.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        handleVerifyOtp();
      }
    });
  }
}

/**
 * Handle sending OTP to email
 */
async function handleSendOtp() {
  try {
    // Hide previous errors
    GrievanceHub.hideError('emailError');
    
    // Get email value
    const email = document.getElementById('adminEmail').value.trim();
    
    // Validate email
    if (!email) {
      GrievanceHub.showError('emailError', 'Please enter your email address');
      return;
    }
    
    if (!isValidEmail(email)) {
      GrievanceHub.showError('emailError', 'Please enter a valid email address');
      return;
    }
    
    // Show loading state
    const sendOtpBtn = document.getElementById('sendOtpBtn');
    const originalText = sendOtpBtn.textContent;
    sendOtpBtn.disabled = true;
    sendOtpBtn.textContent = 'Sending OTP...';
    
    // Make API call
    const response = await GrievanceHub.apiCall('/auth/send-otp', 'POST', {
      email: email,
    });
    
    if (response.success) {
      // Show OTP step
      showOtpStep(email);
      GrievanceHub.showToast('OTP sent to your email', 'info');
    } else {
      GrievanceHub.showError('emailError', response.error || 'Failed to send OTP');
    }
  } catch (error) {
    console.error('[AdminLogin] Error sending OTP:', error);
    GrievanceHub.showError('emailError', 'Error sending OTP. Please check your email and try again.');
  } finally {
    const sendOtpBtn = document.getElementById('sendOtpBtn');
    sendOtpBtn.disabled = false;
    sendOtpBtn.textContent = originalText;
  }
}

/**
 * Handle OTP verification
 */
async function handleVerifyOtp() {
  try {
    // Hide previous errors
    GrievanceHub.hideError('otpError');
    
    // Get values
    const email = document.getElementById('adminEmail').value.trim();
    const otp = document.getElementById('adminOtp').value.trim();
    
    // Validate OTP
    if (!otp) {
      GrievanceHub.showError('otpError', 'Please enter the OTP');
      return;
    }
    
    if (!/^\d{6}$/.test(otp)) {
      GrievanceHub.showError('otpError', 'OTP must be 6 digits');
      return;
    }
    
    // Show loading state
    const verifyBtn = document.getElementById('verifyOtpBtn');
    const originalText = verifyBtn.textContent;
    verifyBtn.disabled = true;
    verifyBtn.textContent = 'Verifying...';
    
    // Make API call
    const response = await GrievanceHub.apiCall('/auth/verify-otp', 'POST', {
      email: email,
      otp: otp,
    });
    
    if (response.success) {
      // Store session token
      GrievanceHub.setAdminToken(response.session_token);
      GrievanceHub.setAdminInfo(response.admin_info);
      
      // Show success message
      GrievanceHub.showToast('Login successful!', 'success');
      
      // Redirect to dashboard
      setTimeout(() => {
        window.location.href = '/admin/dashboard';
      }, 500);
    } else {
      GrievanceHub.showError('otpError', response.error || 'Invalid OTP. Please try again.');
    }
  } catch (error) {
    console.error('[AdminLogin] Error verifying OTP:', error);
    GrievanceHub.showError('otpError', 'Error verifying OTP. Please try again.');
  } finally {
    const verifyBtn = document.getElementById('verifyOtpBtn');
    verifyBtn.disabled = false;
    verifyBtn.textContent = originalText;
  }
}

/**
 * Show email input step
 */
function showEmailStep() {
  const emailStep = document.getElementById('emailStep');
  const otpStep = document.getElementById('otpStep');
  
  if (emailStep) emailStep.classList.add('active');
  if (otpStep) otpStep.classList.remove('active');
  
  // Clear OTP field
  document.getElementById('adminOtp').value = '';
  GrievanceHub.hideError('otpError');
}

/**
 * Show OTP verification step
 */
function showOtpStep(email) {
  const emailStep = document.getElementById('emailStep');
  const otpStep = document.getElementById('otpStep');
  
  if (emailStep) emailStep.classList.remove('active');
  if (otpStep) otpStep.classList.add('active');
  
  // Focus on OTP field
  const otpInput = document.getElementById('adminOtp');
  if (otpInput) {
    setTimeout(() => otpInput.focus(), 100);
  }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Export for use in other modules
 */
const AdminLogin = {
  initializeAdminLogin,
  handleSendOtp,
  handleVerifyOtp,
  showEmailStep,
  showOtpStep,
};
