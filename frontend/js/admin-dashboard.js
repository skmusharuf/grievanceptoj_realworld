// Ensure user is logged in
requireLogin();

// DOM Elements
const adminName = document.getElementById('adminName');
const userInfo = document.getElementById('userInfo');
const navItems = document.querySelectorAll('.nav-item');
const contentSections = document.querySelectorAll('.content-section');
const logoutBtn = document.getElementById('logoutBtn');

// Dashboard elements
const totalComplaintsElem = document.getElementById('totalComplaints');
const pendingComplaintsElem = document.getElementById('pendingComplaints');
const inProgressComplaintsElem = document.getElementById('inProgressComplaints');
const resolvedComplaintsElem = document.getElementById('resolvedComplaints');

// Search and filter
const searchInput = document.getElementById('searchInput');
const statusFilter = document.getElementById('statusFilter');
const categoryFilter = document.getElementById('categoryFilter');

// Modal
const complaintModal = document.getElementById('complaintModal');
const closeModal = document.getElementById('closeModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const updateStatusBtn = document.getElementById('updateStatusBtn');

let currentAdmin = null;
let allComplaints = [];
let currentComplaint = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    loadAdminInfo();
    setupNavigation();
    await loadDashboardData();
    setupEventListeners();
    loadComplaints();
});

function loadAdminInfo() {
    currentAdmin = SessionManager.getAdminInfo();
    adminName.textContent = currentAdmin.name || 'Admin';
    userInfo.textContent = `${currentAdmin.role.replace(/_/g, ' ')} - ${currentAdmin.email}`;
}

function setupNavigation() {
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.dataset.section;
            showSection(section);
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
        });
    });
}

function showSection(sectionId) {
    contentSections.forEach(section => {
        section.classList.remove('active');
    });
    
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
    }
}

async function loadDashboardData() {
    try {
        const response = await apiCall('/api/admin/dashboard-stats', {
            headers: {
                'X-Session-Token': SessionManager.getToken(),
            },
        });
        
        if (response.success) {
            const stats = response.stats;
            totalComplaintsElem.textContent = stats.total_complaints;
            pendingComplaintsElem.textContent = stats.pending;
            inProgressComplaintsElem.textContent = stats.in_progress;
            resolvedComplaintsElem.textContent = stats.resolved;
            
            // Populate category filter
            const categories = Object.keys(stats.by_category);
            categoryFilter.innerHTML = '<option value="">All Categories</option>';
            categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                categoryFilter.appendChild(option);
            });
            
            // Display category chart
            displayCategoryChart(stats.by_category);
        }
    } catch (error) {
        console.error('[v0] Error loading dashboard stats:', error);
    }
}

function displayCategoryChart(categories) {
    const chartDiv = document.getElementById('categoryChart');
    let chartHTML = '<div style="display: grid; gap: 0.5rem;">';
    
    Object.entries(categories).forEach(([category, count]) => {
        const percentage = (count / Object.values(categories).reduce((a, b) => a + b, 0)) * 100;
        chartHTML += `
            <div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="font-size: 0.9rem;">${category}</span>
                    <span style="font-weight: 600;">${count}</span>
                </div>
                <div style="height: 20px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                    <div style="height: 100%; width: ${percentage}%; background: #2563eb;"></div>
                </div>
            </div>
        `;
    });
    
    chartHTML += '</div>';
    chartDiv.innerHTML = chartHTML;
}

async function loadComplaints() {
    try {
        const response = await apiCall('/api/admin/complaints', {
            headers: {
                'X-Session-Token': SessionManager.getToken(),
            },
        });
        
        if (response.success) {
            allComplaints = response.complaints;
            displayComplaints(allComplaints);
            loadRecentComplaints();
        }
    } catch (error) {
        console.error('[v0] Error loading complaints:', error);
    }
}

function displayComplaints(complaints) {
    const complaintsList = document.getElementById('complaintsList');
    
    if (!complaints || complaints.length === 0) {
        complaintsList.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No complaints found</p>';
        return;
    }
    
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Complaint ID</th>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Status</th>
                    <th>Criticality</th>
                    <th>Submitted</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    complaints.forEach(complaint => {
        tableHTML += `
            <tr class="complaint-row" onclick="openComplaintModal(${complaint.id})">
                <td><strong>${complaint.id}</strong></td>
                <td>${complaint.name}</td>
                <td>${complaint.category}</td>
                <td><span class="status-badge ${complaint.status.replace(/\s+/g, '\\ ')}">${complaint.status}</span></td>
                <td>${complaint.criticality}</td>
                <td>${formatDate(complaint.created_at).split(',')[0]}</td>
                <td><button class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">View</button></td>
            </tr>
        `;
    });
    
    tableHTML += '</tbody></table>';
    complaintsList.innerHTML = tableHTML;
}

function loadRecentComplaints() {
    const recentDiv = document.getElementById('recentComplaints');
    const recent = allComplaints.slice(0, 5);
    
    if (recent.length === 0) {
        recentDiv.innerHTML = '<p style="text-align: center; color: #999;">No complaints yet</p>';
        return;
    }
    
    let html = '';
    recent.forEach(complaint => {
        html += `
            <div style="padding: 1rem; border-bottom: 1px solid #e5e7eb; cursor: pointer;" onclick="openComplaintModal(${complaint.id})">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <strong>${complaint.id}</strong>
                    <span class="status-badge ${complaint.status.replace(/\s+/g, '\\ ')}">${complaint.status}</span>
                </div>
                <p style="font-size: 0.9rem; color: #6b7280; margin-bottom: 0.25rem;">${complaint.name}</p>
                <p style="font-size: 0.85rem; color: #9ca3af;">${complaint.category}</p>
            </div>
        `;
    });
    
    recentDiv.innerHTML = html;
}

function setupEventListeners() {
    logoutBtn.addEventListener('click', logout);
    closeModal.addEventListener('click', closeComplaintModal);
    closeModalBtn.addEventListener('click', closeComplaintModal);
    
    // Search and filter
    let filterTimeout;
    searchInput.addEventListener('input', () => {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(filterComplaints, 300);
    });
    
    statusFilter.addEventListener('change', filterComplaints);
    categoryFilter.addEventListener('change', filterComplaints);
}

function filterComplaints() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedStatus = statusFilter.value;
    const selectedCategory = categoryFilter.value;
    
    let filtered = allComplaints.filter(complaint => {
        const matchesSearch = 
            complaint.id.toLowerCase().includes(searchTerm) ||
            complaint.name.toLowerCase().includes(searchTerm) ||
            complaint.email.toLowerCase().includes(searchTerm);
        
        const matchesStatus = !selectedStatus || complaint.status === selectedStatus;
        const matchesCategory = !selectedCategory || complaint.category === selectedCategory;
        
        return matchesSearch && matchesStatus && matchesCategory;
    });
    
    displayComplaints(filtered);
}

function openComplaintModal(complaintId) {
    currentComplaint = allComplaints.find(c => c.id === complaintId);
    
    if (!currentComplaint) {
        // Try numeric ID
        currentComplaint = allComplaints.find(c => c.id.endsWith(complaintId.toString()));
    }
    
    if (currentComplaint) {
        const modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = `
            <div>
                <h3>${currentComplaint.id}</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <label>Name:</label>
                        <p>${currentComplaint.name}</p>
                    </div>
                    <div class="info-item">
                        <label>Email:</label>
                        <p>${currentComplaint.email}</p>
                    </div>
                    <div class="info-item">
                        <label>Phone:</label>
                        <p>${currentComplaint.phone || 'N/A'}</p>
                    </div>
                    <div class="info-item">
                        <label>Category:</label>
                        <p>${currentComplaint.category}</p>
                    </div>
                    <div class="info-item">
                        <label>Criticality:</label>
                        <p>${currentComplaint.criticality}</p>
                    </div>
                    <div class="info-item">
                        <label>Status:</label>
                        <p><span class="status-badge ${currentComplaint.status.replace(/\s+/g, '\\ ')}">${currentComplaint.status}</span></p>
                    </div>
                </div>
                <div style="margin-top: 1rem;">
                    <h4>Description</h4>
                    <p>${currentComplaint.description}</p>
                </div>
                <div style="margin-top: 1rem;">
                    <label>Update Status:</label>
                    <select id="newStatusSelect" style="padding: 0.5rem; margin-top: 0.5rem;">
                        <option value="">Select new status</option>
                        <option value="Pending">Pending</option>
                        <option value="In Progress">In Progress</option>
                        <option value="Resolved">Resolved</option>
                    </select>
                    <textarea id="statusNotes" placeholder="Add notes (optional)" style="margin-top: 0.5rem; padding: 0.5rem; width: 100%;"></textarea>
                </div>
            </div>
        `;
        
        complaintModal.style.display = 'flex';
    }
}

function closeComplaintModal() {
    complaintModal.style.display = 'none';
    currentComplaint = null;
}

updateStatusBtn.addEventListener('click', async () => {
    if (!currentComplaint) return;
    
    const newStatus = document.getElementById('newStatusSelect').value;
    const notes = document.getElementById('statusNotes').value.trim();
    
    if (!newStatus) {
        alert('Please select a new status');
        return;
    }
    
    try {
        updateStatusBtn.disabled = true;
        updateStatusBtn.textContent = 'Updating...';
        
        // Extract numeric ID from complaint ID
        const numericId = currentComplaint.id.match(/\d+/)?.[0] || currentComplaint.id;
        
        const response = await apiCall(`/api/admin/complaints/${numericId}/status`, {
            method: 'PUT',
            headers: {
                'X-Session-Token': SessionManager.getToken(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus, notes }),
        });
        
        if (response.success) {
            await loadComplaints();
            await loadDashboardData();
            closeComplaintModal();
            alert('Status updated successfully');
        }
    } catch (error) {
        alert('Error updating status: ' + error.message);
    } finally {
        updateStatusBtn.disabled = false;
        updateStatusBtn.textContent = 'Update Status';
    }
});

function logout() {
    SessionManager.clearToken();
    SessionManager.clearAdminInfo();
    window.location.href = 'admin-login.html';
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === complaintModal) {
        closeComplaintModal();
    }
});
