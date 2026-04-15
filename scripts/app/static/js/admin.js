/**
 * Admin Dashboard Module
 * Handles admin dashboard functionality and complaint management
 */

let allComplaints = [];
let charts = {};

/**
 * Initialize admin dashboard
 */
function initializeAdminDashboard() {
  // Check authentication
  GrievanceHub.requireAuth();
  
  // Load admin info
  loadAdminInfo();
  
  // Setup filters
  setupFilters();
  
  // Setup buttons
  setupButtons();
  
  // Load initial data
  loadDashboardData();
}

/**
 * Load and display admin info
 */
function loadAdminInfo() {
  const adminInfo = GrievanceHub.getAdminInfo();
  
  if (adminInfo) {
    const adminNameEl = document.getElementById('adminName');
    if (adminNameEl) {
      adminNameEl.textContent = `${adminInfo.name} (${adminInfo.role})`;
    }
  }
}

/**
 * Setup filter event listeners
 */
function setupFilters() {
  const applyFiltersBtn = document.getElementById('applyFiltersBtn');
  
  if (applyFiltersBtn) {
    applyFiltersBtn.addEventListener('click', applyFilters);
  }
  
  // Debounce search input
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', GrievanceHub.debounce(applyFilters, 300));
  }
}

/**
 * Setup button event listeners
 */
function setupButtons() {
  const logoutBtn = document.getElementById('logoutBtn');
  const refreshBtn = document.getElementById('refreshBtn');
  
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }
  
  if (refreshBtn) {
    refreshBtn.addEventListener('click', loadDashboardData);
  }
}

/**
 * Load dashboard data
 */
async function loadDashboardData() {
  try {
    // Load complaints
    await loadComplaints();
    
    // Load filter options
    await loadFilterOptions();
    
    // Update stats
    updateStats();
    
    // Update charts
    updateCharts();
  } catch (error) {
    console.error('[AdminDashboard] Error loading data:', error);
  }
}

/**
 * Load complaints from API
 */
async function loadComplaints() {
  try {
    const response = await GrievanceHub.apiCall('/admin/complaints');
    
    if (response.success) {
      allComplaints = response.complaints || [];
      displayComplaints(allComplaints);
    }
  } catch (error) {
    console.error('[AdminDashboard] Error loading complaints:', error);
  }
}

/**
 * Load filter options
 */
async function loadFilterOptions() {
  try {
    const response = await GrievanceHub.apiCall('/admin/departments');
    
    if (response.departments) {
      const deptSelect = document.getElementById('departmentFilter');
      if (deptSelect) {
        response.departments.forEach(dept => {
          const option = document.createElement('option');
          option.value = dept;
          option.textContent = dept;
          deptSelect.appendChild(option);
        });
      }
    }
    
    const zoneResponse = await GrievanceHub.apiCall('/zones');
    if (zoneResponse.zones) {
      const zoneSelect = document.getElementById('zoneFilter');
      if (zoneSelect) {
        zoneResponse.zones.forEach(zone => {
          const option = document.createElement('option');
          option.value = zone.id;
          option.textContent = `${zone.zone_number} - ${zone.zone_name}`;
          zoneSelect.appendChild(option);
        });
      }
    }
  } catch (error) {
    console.error('[AdminDashboard] Error loading filters:', error);
  }
}

/**
 * Apply filters
 */
function applyFilters() {
  let filtered = [...allComplaints];
  
  // Department filter
  const dept = document.getElementById('departmentFilter').value;
  if (dept !== 'all') {
    filtered = filtered.filter(c => c.department === dept);
  }
  
  // Status filter
  const status = document.getElementById('statusFilter').value;
  if (status !== 'all') {
    filtered = filtered.filter(c => c.status?.toLowerCase() === status);
  }
  
  // Zone filter
  const zone = document.getElementById('zoneFilter').value;
  if (zone !== 'all') {
    filtered = filtered.filter(c => c.zone_id == zone);
  }
  
  // Search filter
  const search = document.getElementById('searchInput').value.toLowerCase();
  if (search) {
    filtered = filtered.filter(c =>
      c.id.toLowerCase().includes(search) ||
      c.name.toLowerCase().includes(search) ||
      c.email.toLowerCase().includes(search)
    );
  }
  
  displayComplaints(filtered);
}

/**
 * Display complaints in table
 */
function displayComplaints(complaints) {
  const tbody = document.getElementById('tableBody');
  
  if (!tbody) return;
  
  if (complaints.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px;">No complaints found</td></tr>';
    return;
  }
  
  tbody.innerHTML = complaints.map(complaint => `
    <tr onclick="viewComplaintDetails('${complaint.id}')">
      <td>${complaint.id}</td>
      <td>${complaint.name}</td>
      <td>${complaint.category || 'N/A'}</td>
      <td><span class="badge ${getStatusClass(complaint.status)}">${complaint.status}</span></td>
      <td><span class="badge ${complaint.criticality === 'Critical' ? 'critical' : 'resolved'}">${complaint.criticality}</span></td>
      <td>${complaint.zone_name || 'N/A'}</td>
      <td>${new Date(complaint.created_at).toLocaleDateString()}</td>
      <td><button class="table-action-btn" onclick="event.stopPropagation(); viewComplaintDetails('${complaint.id}')">View</button></td>
    </tr>
  `).join('');
}

/**
 * View complaint details in modal
 */
function viewComplaintDetails(complaintId) {
  const complaint = allComplaints.find(c => c.id === complaintId);
  
  if (!complaint) return;
  
  // Populate modal
  document.getElementById('modalId').textContent = complaint.id;
  document.getElementById('modalName').textContent = complaint.name;
  document.getElementById('modalEmail').textContent = complaint.email;
  document.getElementById('modalPhone').textContent = complaint.phone;
  document.getElementById('modalCategory').textContent = complaint.category || 'N/A';
  document.getElementById('modalDescription').textContent = complaint.description;
  document.getElementById('modalStatus').value = complaint.status?.toLowerCase().replace(/\s+/g, '_');
  
  // Setup modal buttons
  const updateBtn = document.getElementById('updateStatusBtn');
  if (updateBtn) {
    updateBtn.onclick = () => updateComplaintStatus(complaintId);
  }
  
  const closeBtn = document.getElementById('closeModalBtn');
  if (closeBtn) {
    closeBtn.onclick = closeModal;
  }
  
  const closeIcon = document.querySelector('.modal-close');
  if (closeIcon) {
    closeIcon.onclick = closeModal;
  }
  
  // Show modal
  const modal = document.getElementById('detailsModal');
  if (modal) {
    modal.style.display = 'flex';
  }
}

/**
 * Update complaint status
 */
async function updateComplaintStatus(complaintId) {
  try {
    const newStatus = document.getElementById('modalStatus').value;
    const updateBtn = document.getElementById('updateStatusBtn');
    
    updateBtn.disabled = true;
    updateBtn.textContent = 'Updating...';
    
    const response = await GrievanceHub.apiCall(`/admin/complaints/${complaintId}`, 'PUT', {
      status: newStatus,
    });
    
    if (response.success) {
      GrievanceHub.showToast('Status updated successfully', 'success');
      
      // Reload data
      await loadDashboardData();
      
      closeModal();
    } else {
      GrievanceHub.showToast('Failed to update status', 'error');
    }
  } catch (error) {
    console.error('[AdminDashboard] Error updating status:', error);
    GrievanceHub.showToast('Error updating status', 'error');
  } finally {
    const updateBtn = document.getElementById('updateStatusBtn');
    updateBtn.disabled = false;
    updateBtn.textContent = 'Update Status';
  }
}

/**
 * Close modal
 */
function closeModal() {
  const modal = document.getElementById('detailsModal');
  if (modal) {
    modal.style.display = 'none';
  }
}

/**
 * Update statistics
 */
function updateStats() {
  const total = allComplaints.length;
  const pending = allComplaints.filter(c => c.status?.toLowerCase() === 'pending').length;
  const inProgress = allComplaints.filter(c => c.status?.toLowerCase().includes('progress')).length;
  const resolved = allComplaints.filter(c => c.status?.toLowerCase() === 'resolved').length;
  
  document.getElementById('totalComplaints').textContent = total;
  document.getElementById('pendingComplaints').textContent = pending;
  document.getElementById('inProgressComplaints').textContent = inProgress;
  document.getElementById('resolvedComplaints').textContent = resolved;
}

/**
 * Update charts
 */
function updateCharts() {
  updateCategoryChart();
  updateStatusChart();
}

/**
 * Update category chart
 */
function updateCategoryChart() {
  const categoryData = {};
  
  allComplaints.forEach(c => {
    const cat = c.category || 'Uncategorized';
    categoryData[cat] = (categoryData[cat] || 0) + 1;
  });
  
  const ctx = document.getElementById('categoryChart');
  if (!ctx) return;
  
  // Destroy existing chart
  if (charts.category) {
    charts.category.destroy();
  }
  
  charts.category = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: Object.keys(categoryData),
      datasets: [{
        data: Object.values(categoryData),
        backgroundColor: [
          '#3b82f6',
          '#10b981',
          '#f59e0b',
          '#ef4444',
          '#8b5cf6',
          '#06b6d4',
        ],
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: '#cbd5e1',
          },
        },
      },
    },
  });
}

/**
 * Update status chart
 */
function updateStatusChart() {
  const pending = allComplaints.filter(c => c.status?.toLowerCase() === 'pending').length;
  const inProgress = allComplaints.filter(c => c.status?.toLowerCase().includes('progress')).length;
  const resolved = allComplaints.filter(c => c.status?.toLowerCase() === 'resolved').length;
  
  const ctx = document.getElementById('statusChart');
  if (!ctx) return;
  
  // Destroy existing chart
  if (charts.status) {
    charts.status.destroy();
  }
  
  charts.status = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Pending', 'In Progress', 'Resolved'],
      datasets: [{
        data: [pending, inProgress, resolved],
        backgroundColor: ['#f59e0b', '#3b82f6', '#10b981'],
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: '#cbd5e1',
          },
        },
      },
    },
  });
}

/**
 * Get status CSS class
 */
function getStatusClass(status) {
  const statusMap = {
    'pending': 'pending',
    'in_progress': 'inprogress',
    'in-progress': 'inprogress',
    'resolved': 'resolved',
  };
  
  return statusMap[status?.toLowerCase()] || 'pending';
}

/**
 * Handle logout
 */
function handleLogout() {
  GrievanceHub.clearAdminSession();
  GrievanceHub.showToast('Logged out successfully', 'info');
  
  setTimeout(() => {
    window.location.href = '/admin/login';
  }, 500);
}

/**
 * Export for use in other modules
 */
const AdminDashboard = {
  initializeAdminDashboard,
  loadDashboardData,
  viewComplaintDetails,
  handleLogout,
};
