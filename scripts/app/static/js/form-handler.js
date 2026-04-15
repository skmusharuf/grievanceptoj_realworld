/**
 * Form Handler Module
 * Handles complaint form submission and validation
 */

/**
 * Initialize form handler
 */
function initializeFormHandler() {
  const form = document.getElementById('complaintForm');
  
  if (!form) return;
  
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    await handleComplaintSubmit();
  });
  
  // Real-time validation
  setupFormValidation();
}

/**
 * Setup real-time form validation
 */
function setupFormValidation() {
  const requiredFields = ['name', 'email', 'phone', 'address', 'zone', 'description'];
  
  requiredFields.forEach(fieldId => {
    const field = document.getElementById(fieldId);
    if (field) {
      field.addEventListener('blur', function() {
        validateField(this);
      });
      
      field.addEventListener('input', function() {
        if (this.classList.contains('error')) {
          validateField(this);
        }
      });
    }
  });
}

/**
 * Validate individual field
 */
function validateField(field) {
  const fieldId = field.id;
  const value = field.value.trim();
  let isValid = true;
  
  switch (fieldId) {
    case 'name':
      isValid = value.length >= 3;
      break;
    case 'email':
      isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
      break;
    case 'phone':
      isValid = /^\d{10}$/.test(value.replace(/\D/g, ''));
      break;
    case 'address':
      isValid = value.length >= 10;
      break;
    case 'zone':
      isValid = value !== '';
      break;
    case 'description':
      isValid = value.length >= 20;
      break;
  }
  
  if (isValid) {
    field.classList.remove('error');
  } else {
    field.classList.add('error');
  }
  
  return isValid;
}

/**
 * Validate entire form
 */
function validateForm() {
  const requiredFields = ['name', 'email', 'phone', 'address', 'zone', 'description'];
  let isValid = true;
  
  requiredFields.forEach(fieldId => {
    const field = document.getElementById(fieldId);
    if (field && !validateField(field)) {
      isValid = false;
    }
  });
  
  return isValid;
}

/**
 * Get form data
 */
function getFormData() {
  const formData = {
    name: document.getElementById('name').value.trim(),
    email: document.getElementById('email').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    full_address: document.getElementById('address').value.trim(),
    locality_name: document.getElementById('zone').options[document.getElementById('zone').selectedIndex].text,
    zone_id: parseInt(document.getElementById('zone').value),
    description: document.getElementById('description').value.trim(),
  };
  
  return formData;
}

/**
 * Handle complaint form submission
 */
async function handleComplaintSubmit() {
  // Validate form
  if (!validateForm()) {
    GrievanceHub.showError('errorAlert', 'Please fill all fields correctly');
    return;
  }
  
  // Get form data
  const formData = getFormData();
  
  try {
    // Show loading state
    const submitBtn = document.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    // Make API call
    const response = await GrievanceHub.apiCall('/complaints/submit', 'POST', formData);
    
    if (response.success) {
      // Show success message
      GrievanceHub.showToast('Complaint submitted successfully!', 'success');
      
      // Show complaint ID
      showSuccessMessage(response.complaint_id);
      
      // Reset form
      document.getElementById('complaintForm').reset();
      document.getElementById('description').value = '';
      
      // Redirect after delay
      setTimeout(() => {
        window.location.href = `/track?id=${response.complaint_id}`;
      }, 2000);
    } else {
      GrievanceHub.showError('errorAlert', response.error || 'Failed to submit complaint');
    }
  } catch (error) {
    console.error('[FormHandler] Error:', error);
    GrievanceHub.showError('errorAlert', 'An error occurred. Please try again.');
  } finally {
    // Restore button
    const submitBtn = document.querySelector('button[type="submit"]');
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
  }
}

/**
 * Show success message with complaint ID
 */
function showSuccessMessage(complaintId) {
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-success';
  alertDiv.innerHTML = `
    <div>
      <p style="margin: 0; font-weight: 600;">Complaint Submitted Successfully!</p>
      <p style="margin: 5px 0 0 0; font-size: 14px;">Your Complaint ID: <code style="background: var(--bg-tertiary); padding: 2px 4px; border-radius: 3px;">${complaintId}</code></p>
      <p style="margin: 5px 0 0 0; font-size: 14px;">Save this ID to track your complaint status.</p>
    </div>
  `;
  
  const form = document.getElementById('complaintForm');
  form.parentNode.insertBefore(alertDiv, form);
}

/**
 * Reset form to initial state
 */
function resetForm() {
  const form = document.getElementById('complaintForm');
  if (form) {
    form.reset();
    
    // Clear error states
    const fields = form.querySelectorAll('input, textarea, select');
    fields.forEach(field => {
      field.classList.remove('error');
    });
  }
  
  // Hide error message
  GrievanceHub.hideError('errorAlert');
}

/**
 * Export for use in other modules
 */
const FormHandler = {
  initializeFormHandler,
  getFormData,
  validateForm,
  resetForm,
};
