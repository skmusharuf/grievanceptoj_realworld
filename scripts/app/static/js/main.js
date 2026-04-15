/**
 * GrievanceHub - Main JavaScript Module
 * Global utilities and initialization
 */

// API Configuration
const API_BASE_URL = '/api';

/**
 * Make API calls with proper error handling
 */
async function apiCall(endpoint, method = 'GET', data = null) {
  try {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data && (method === 'POST' || method === 'PUT')) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('[GrievanceHub] API Error:', error);
    throw error;
  }
}

/**
 * Show error message
 */
function showError(elementId, message) {
  const errorElement = document.getElementById(elementId);
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = 'block';
  }
}

/**
 * Hide error message
 */
function hideError(elementId) {
  const errorElement = document.getElementById(elementId);
  if (errorElement) {
    errorElement.style.display = 'none';
  }
}

/**
 * Format date to readable string
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Generate random ID for complaints
 */
function generateComplaintId() {
  const timestamp = Date.now().toString().slice(-6);
  const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
  return `CMP${timestamp}${random}`;
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  document.body.appendChild(toast);
  
  // Auto-remove after 3 seconds
  setTimeout(() => {
    toast.remove();
  }, 3000);
}

/**
 * Check if element is visible in viewport
 */
function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Get admin session token from localStorage
 */
function getAdminToken() {
  return localStorage.getItem('adminSessionToken');
}

/**
 * Set admin session token
 */
function setAdminToken(token) {
  localStorage.setItem('adminSessionToken', token);
}

/**
 * Clear admin session
 */
function clearAdminSession() {
  localStorage.removeItem('adminSessionToken');
  localStorage.removeItem('adminInfo');
}

/**
 * Get admin info from localStorage
 */
function getAdminInfo() {
  const info = localStorage.getItem('adminInfo');
  return info ? JSON.parse(info) : null;
}

/**
 * Set admin info
 */
function setAdminInfo(info) {
  localStorage.setItem('adminInfo', JSON.stringify(info));
}

/**
 * Check if user is authenticated admin
 */
function isAdminAuthenticated() {
  return !!getAdminToken();
}

/**
 * Redirect to login if not authenticated
 */
function requireAuth() {
  if (!isAdminAuthenticated()) {
    window.location.href = '/admin/login';
  }
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
  const tooltips = document.querySelectorAll('[data-tooltip]');
  tooltips.forEach(el => {
    el.addEventListener('mouseenter', function() {
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      tooltip.textContent = this.getAttribute('data-tooltip');
      document.body.appendChild(tooltip);
      
      const rect = this.getBoundingClientRect();
      tooltip.style.top = (rect.top - 40) + 'px';
      tooltip.style.left = rect.left + 'px';
    });
  });
}

/**
 * Page initialization on DOM ready
 */
document.addEventListener('DOMContentLoaded', function() {
  // Initialize tooltips
  initializeTooltips();
  
  // Setup global error handling
  window.addEventListener('error', function(event) {
    console.error('[GrievanceHub] Unexpected error:', event.error);
  });
  
  // Setup unhandled promise rejection
  window.addEventListener('unhandledrejection', function(event) {
    console.error('[GrievanceHub] Unhandled promise rejection:', event.reason);
  });
});

/**
 * Export for use in other modules
 */
const GrievanceHub = {
  apiCall,
  showError,
  hideError,
  formatDate,
  generateComplaintId,
  showToast,
  isElementInViewport,
  debounce,
  getAdminToken,
  setAdminToken,
  clearAdminSession,
  getAdminInfo,
  setAdminInfo,
  isAdminAuthenticated,
  requireAuth,
};
