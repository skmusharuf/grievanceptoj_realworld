// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// Helper function to make API calls
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Merge options
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {}),
        },
    };

    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `API Error: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('[v0] API Error:', error);
        throw error;
    }
}

// Session management
const SessionManager = {
    getToken: () => localStorage.getItem('adminSessionToken'),
    setToken: (token) => localStorage.setItem('adminSessionToken', token),
    clearToken: () => localStorage.removeItem('adminSessionToken'),
    getAdminInfo: () => JSON.parse(localStorage.getItem('adminInfo') || '{}'),
    setAdminInfo: (info) => localStorage.setItem('adminInfo', JSON.stringify(info)),
    clearAdminInfo: () => localStorage.removeItem('adminInfo'),
    isLoggedIn: () => !!localStorage.getItem('adminSessionToken'),
};

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

function showError(message, elementId = 'errorMessage') {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }
}

function showSuccess(message) {
    console.log('[v0] Success:', message);
    // Can be enhanced with toast notifications
}

// Redirect if not logged in
function requireLogin() {
    if (!SessionManager.isLoggedIn()) {
        window.location.href = 'admin-login.html';
    }
}

// Redirect if logged in
function requireLogout() {
    if (SessionManager.isLoggedIn()) {
        window.location.href = 'admin-dashboard.html';
    }
}
