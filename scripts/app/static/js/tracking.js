/**
 * Tracking Module
 * Handles complaint tracking and real-time updates
 */

/**
 * Initialize tracking functionality
 */
function initializeTracking() {
  const trackBtn = document.getElementById('trackBtn');
  
  if (trackBtn) {
    trackBtn.addEventListener('click', handleTrackComplaint);
  }
  
  // Allow Enter key to submit
  const otpInput = document.getElementById('otp');
  if (otpInput) {
    otpInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        handleTrackComplaint();
      }
    });
  }
}

/**
 * Handle complaint tracking
 */
async function handleTrackComplaint() {
  try {
    // Clear previous errors
    GrievanceHub.hideError('trackError');
    
    // Get input values
    const complaintId = document.getElementById('complaintId').value.trim();
    const email = document.getElementById('trackEmail').value.trim();
    const otp = document.getElementById('otp').value.trim();
    
    // Validate inputs
    if (!complaintId || !email || !otp) {
      GrievanceHub.showError('trackError', 'Please enter complaint ID, email, and OTP');
      return;
    }
    
    // Validate email format
    if (!isValidEmail(email)) {
      GrievanceHub.showError('trackError', 'Please enter a valid email address');
      return;
    }
    
    // Show loading state
    const trackBtn = document.getElementById('trackBtn');
    const originalText = trackBtn.textContent;
    trackBtn.disabled = true;
    trackBtn.textContent = 'Tracking...';
    
    // Make API call
    const response = await GrievanceHub.apiCall('/complaints/track', 'POST', {
      complaint_id: complaintId,
      email: email,
      otp: otp,
    });
    
    if (response.success) {
      // Display complaint details
      displayComplaintDetails(response.complaint);
      GrievanceHub.hideError('trackError');
    } else {
      GrievanceHub.showError('trackError', response.error || 'Complaint not found or invalid OTP');
    }
  } catch (error) {
    console.error('[Tracking] Error:', error);
    GrievanceHub.showError('trackError', 'Error tracking complaint. Please try again.');
  } finally {
    const trackBtn = document.getElementById('trackBtn');
    trackBtn.disabled = false;
    trackBtn.textContent = originalText;
  }
}

/**
 * Display complaint details
 */
function displayComplaintDetails(complaint) {
  const detailsDiv = document.getElementById('complaintDetails');
  
  if (!detailsDiv) return;
  
  // Populate fields
  document.getElementById('displayId').textContent = complaint.id;
  document.getElementById('displayCategory').textContent = complaint.category || 'Not categorized';
  document.getElementById('displayStatus').textContent = complaint.status;
  document.getElementById('displayCreated').textContent = GrievanceHub.formatDate(complaint.created_at);
  document.getElementById('displayUpdated').textContent = GrievanceHub.formatDate(complaint.updated_at);
  document.getElementById('displayDescription').textContent = complaint.description;
  
  // Set status badge
  const statusBadge = document.getElementById('statusBadge');
  const statusClass = getStatusClass(complaint.status);
  statusBadge.className = `badge ${statusClass}`;
  statusBadge.textContent = complaint.status.replace(/_/g, ' ').toUpperCase();
  
  // Set criticality badge
  const criticalityBadge = document.getElementById('displayCriticality');
  const criticalityClass = complaint.criticality === 'Critical' ? 'critical' : 'resolved';
  criticalityBadge.className = `badge ${criticalityClass}`;
  criticalityBadge.textContent = complaint.criticality;
  
  // Show critical alert if needed
  const criticalAlert = document.getElementById('criticalAlert');
  if (complaint.criticality === 'Critical') {
    criticalAlert.style.display = 'block';
  } else {
    criticalAlert.style.display = 'none';
  }
  
  // Update timeline
  updateTimeline(complaint.status, complaint.updated_at);
  
  // Show details section
  detailsDiv.style.display = 'block';
  
  // Scroll to details
  detailsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Get status CSS class
 */
function getStatusClass(status) {
  const statusMap = {
    'pending': 'pending',
    'in_progress': 'in-progress',
    'in-progress': 'in-progress',
    'resolved': 'resolved',
  };
  
  return statusMap[status?.toLowerCase()] || 'pending';
}

/**
 * Update timeline display
 */
function updateTimeline(status, updatedAt) {
  const inProgressTimeline = document.getElementById('inProgressTimeline');
  const resolvedTimeline = document.getElementById('resolvedTimeline');
  const timelineSubmitted = document.getElementById('timelineSubmitted');
  
  // Show submitted
  if (timelineSubmitted) {
    timelineSubmitted.textContent = GrievanceHub.formatDate(new Date());
  }
  
  // Show in progress if applicable
  if (status === 'in_progress' || status === 'In Progress' || status === 'resolved') {
    if (inProgressTimeline) {
      inProgressTimeline.style.display = 'flex';
    }
  } else {
    if (inProgressTimeline) {
      inProgressTimeline.style.display = 'none';
    }
  }
  
  // Show resolved if applicable
  if (status === 'resolved' || status === 'Resolved') {
    if (resolvedTimeline) {
      resolvedTimeline.style.display = 'flex';
      const timelineResolved = document.getElementById('timelineResolved');
      if (timelineResolved) {
        timelineResolved.textContent = GrievanceHub.formatDate(updatedAt);
      }
    }
  } else {
    if (resolvedTimeline) {
      resolvedTimeline.style.display = 'none';
    }
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
 * Clear tracking form
 */
function clearTrackingForm() {
  document.getElementById('complaintId').value = '';
  document.getElementById('trackEmail').value = '';
  document.getElementById('otp').value = '';
  GrievanceHub.hideError('trackError');
  
  const detailsDiv = document.getElementById('complaintDetails');
  if (detailsDiv) {
    detailsDiv.style.display = 'none';
  }
}

/**
 * Start polling for updates (optional)
 */
function pollForUpdates(complaintId, email, otp, interval = 5000) {
  setInterval(async () => {
    try {
      const response = await GrievanceHub.apiCall('/complaints/track', 'POST', {
        complaint_id: complaintId,
        email: email,
        otp: otp,
      });
      
      if (response.success) {
        displayComplaintDetails(response.complaint);
      }
    } catch (error) {
      console.error('[Tracking] Poll error:', error);
    }
  }, interval);
}

/**
 * Export for use in other modules
 */
const Tracking = {
  initializeTracking,
  handleTrackComplaint,
  displayComplaintDetails,
  clearTrackingForm,
  pollForUpdates,
};
