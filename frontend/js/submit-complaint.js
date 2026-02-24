// DOM Elements
const complaintForm = document.getElementById('complaintForm');
const zoneSelect = document.getElementById('zone');
const areaSelect = document.getElementById('area');
const descriptionInput = document.getElementById('description');
const classificationResult = document.getElementById('classificationResult');
const classifiedCategory = document.getElementById('classified_category');
const classifiedCriticality = document.getElementById('classified_criticality');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');
const submitBtn = document.getElementById('submitBtn');

let zones = [];
let areas = [];

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadZones();
    await loadAreas();
    setupEventListeners();
});

async function loadZones() {
    try {
        const response = await apiCall('/api/zones');
        zones = response.zones || [];
        
        zoneSelect.innerHTML = '<option value="">Select a zone</option>';
        zones.forEach(zone => {
            const option = document.createElement('option');
            option.value = zone.id;
            option.textContent = `${zone.zone_number}. ${zone.zone_name}`;
            zoneSelect.appendChild(option);
        });
    } catch (error) {
        console.error('[v0] Error loading zones:', error);
    }
}

async function loadAreas() {
    try {
        const response = await apiCall('/api/areas');
        areas = response.areas || [];
        populateAreaSelect();
    } catch (error) {
        console.error('[v0] Error loading areas:', error);
    }
}

function populateAreaSelect() {
    const selectedZoneId = zoneSelect.value;
    
    areaSelect.innerHTML = '<option value="">Select a locality</option>';
    
    const filteredAreas = selectedZoneId
        ? areas.filter(area => area.zone_id === parseInt(selectedZoneId))
        : areas;
    
    filteredAreas.forEach(area => {
        const option = document.createElement('option');
        option.value = area.id;
        option.textContent = area.display_name;
        areaSelect.appendChild(option);
    });
}

async function classifyComplaint() {
    const description = descriptionInput.value.trim();
    
    if (!description || description.length < 3) {
        classificationResult.style.display = 'none';
        return;
    }
    
    try {
        const response = await apiCall('/api/complaints/classify', {
            method: 'POST',
            body: JSON.stringify({ description }),
        });
        
        if (response.success) {
            classifiedCategory.textContent = response.category;
            classifiedCriticality.textContent = response.criticality;
            classificationResult.style.display = 'block';
        }
    } catch (error) {
        console.error('[v0] Classification error:', error);
    }
}

function setupEventListeners() {
    zoneSelect.addEventListener('change', populateAreaSelect);
    
    // Debounce classification
    let classifyTimeout;
    descriptionInput.addEventListener('input', () => {
        clearTimeout(classifyTimeout);
        classifyTimeout = setTimeout(classifyComplaint, 500);
    });
}

complaintForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    submitBtn.disabled = true;
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
    
    try {
        const formData = {
            name: document.getElementById('name').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim() || null,
            aadhar: document.getElementById('aadhar').value.trim() || null,
            description: descriptionInput.value.trim(),
            full_address: document.getElementById('full_address').value.trim() || '',
            area_id: areaSelect.value ? parseInt(areaSelect.value) : null,
        };
        
        // Validate required fields
        if (!formData.name || !formData.email || !formData.description) {
            throw new Error('Please fill in all required fields');
        }
        
        const response = await apiCall('/api/complaints/submit', {
            method: 'POST',
            body: JSON.stringify(formData),
        });
        
        if (response.success) {
            // Show success message
            document.getElementById('complaintId').textContent = response.complaint_id;
            document.getElementById('submittedCategory').textContent = response.category;
            document.getElementById('trackingOTP').textContent = response.otp || 'Sent to your email';
            
            successMessage.style.display = 'block';
            complaintForm.style.display = 'none';
        }
    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
    }
});
