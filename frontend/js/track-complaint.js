// DOM Elements
const trackForm = document.getElementById('trackForm');
const complaintResult = document.getElementById('complaintResult');
const errorMessage = document.getElementById('errorMessage');
const loading = document.getElementById('loading');
const trackBtn = document.getElementById('trackBtn');

trackForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const complaintId = document.getElementById('complaint_id').value.trim();
    const email = document.getElementById('email').value.trim();
    const otp = document.getElementById('otp').value.trim();
    
    if (!complaintId || !email) {
        errorMessage.textContent = 'Please enter Complaint ID and Email';
        errorMessage.style.display = 'block';
        return;
    }
    
    trackBtn.disabled = true;
    loading.style.display = 'block';
    errorMessage.style.display = 'none';
    complaintResult.style.display = 'none';
    
    try {
        const response = await apiCall('/api/complaints/track', {
            method: 'POST',
            body: JSON.stringify({
                complaint_id: complaintId,
                email: email,
                otp: otp || '000000', // Use dummy OTP if not provided
            }),
        });
        
        if (response.success) {
            displayComplaint(response.complaint);
            displayHistory(response.history);
            complaintResult.style.display = 'block';
        }
    } catch (error) {
        errorMessage.textContent = error.message || 'Failed to track complaint. Please check your details.';
        errorMessage.style.display = 'block';
    } finally {
        loading.style.display = 'none';
        trackBtn.disabled = false;
    }
});

function displayComplaint(complaint) {
    document.getElementById('resultComplaintId').textContent = complaint.id;
    document.getElementById('resultName').textContent = complaint.name;
    document.getElementById('resultEmail').textContent = complaint.email;
    document.getElementById('resultPhone').textContent = complaint.phone || 'Not provided';
    document.getElementById('resultCategory').textContent = complaint.category || 'Unclassified';
    document.getElementById('resultCriticality').textContent = complaint.criticality;
    document.getElementById('resultLocality').textContent = complaint.locality_name || 'Not specified';
    document.getElementById('resultZone').textContent = complaint.zone_name || 'Not assigned';
    document.getElementById('resultDescription').textContent = complaint.description;
    
    // Status badge with dynamic class
    const statusElement = document.getElementById('resultStatus');
    statusElement.textContent = complaint.status;
    statusElement.className = `status-badge ${complaint.status.replace(/\s+/g, '\\ ')}`;
}

function displayHistory(history) {
    const timeline = document.getElementById('statusTimeline');
    timeline.innerHTML = '';
    
    if (!history || history.length === 0) {
        timeline.innerHTML = '<p style="color: #999;">No status updates yet</p>';
        return;
    }
    
    history.forEach((item) => {
        const timelineItem = document.createElement('div');
        timelineItem.className = 'timeline-item';
        
        const title = document.createElement('div');
        title.className = 'timeline-item-title';
        title.textContent = item.new_status;
        
        const time = document.createElement('div');
        time.className = 'timeline-item-time';
        time.textContent = formatDate(item.created_at);
        
        timelineItem.appendChild(title);
        timelineItem.appendChild(time);
        
        if (item.notes) {
            const notes = document.createElement('div');
            notes.className = 'timeline-item-notes';
            notes.textContent = item.notes;
            timelineItem.appendChild(notes);
        }
        
        timeline.appendChild(timelineItem);
    });
}
