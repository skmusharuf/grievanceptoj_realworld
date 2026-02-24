// Global state
let currentStep = 1;
let formData = {
    name: '',
    phone: '',
    email: '',
    aadhar: '',
    area_id: null,
    full_address: '',
    description: ''
};
let selectedArea = null;
let isListening = false;
let currentLanguage = 'en-IN';
let recognitionRef = null;

const API_URL = 'http://localhost:5000';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeSpeechRecognition();
    setupEventListeners();
    updateProgressBar();
});

// Setup event listeners
function setupEventListeners() {
    // Area search
    document.getElementById('areaSearch').addEventListener('input', debounce(searchAreas, 300));
    document.getElementById('areaSearch').addEventListener('focus', showAreaDropdown);
    
    // Form inputs
    document.getElementById('name').addEventListener('change', (e) => formData.name = e.target.value);
    document.getElementById('phone').addEventListener('change', (e) => formData.phone = e.target.value);
    document.getElementById('email').addEventListener('change', (e) => formData.email = e.target.value);
    document.getElementById('aadhar').addEventListener('change', (e) => formData.aadhar = e.target.value);
    document.getElementById('full_address').addEventListener('change', (e) => formData.full_address = e.target.value);
    document.getElementById('description').addEventListener('change', (e) => formData.description = e.target.value);
    document.getElementById('otp').addEventListener('change', (e) => document.otpValue = e.target.value);
}

// Area search with dropdown
async function searchAreas() {
    const searchTerm = document.getElementById('areaSearch').value;
    if (searchTerm.length < 2) {
        document.getElementById('areaDropdown').style.display = 'none';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/areas?search=${encodeURIComponent(searchTerm)}`);
        const data = await response.json();
        
        if (data.success) {
            displayAreaOptions(data.areas);
        }
    } catch (error) {
        console.error('[v0] Error searching areas:', error);
    }
}

function displayAreaOptions(areas) {
    const dropdown = document.getElementById('areaDropdown');
    dropdown.innerHTML = '';
    
    if (areas.length === 0) {
        dropdown.innerHTML = '<div style="padding: 1rem; text-align: center; color: #cbd5e1;">No areas found</div>';
        dropdown.style.display = 'block';
        return;
    }

    areas.forEach(area => {
        const item = document.createElement('button');
        item.type = 'button';
        item.className = 'w-full px-4 py-3 text-left hover:bg-slate-600 transition-colors border-b border-slate-600 last:border-0 text-white';
        item.innerHTML = `
            <div class="flex items-start gap-2">
                <svg class="h-4 w-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                </svg>
                <div>
                    <p class="text-white font-medium">${area.area_name}</p>
                    <p class="text-xs text-slate-400">
                        Zone ${area.zone_number}: ${area.zone_name} | Circle: ${area.circle_name}
                    </p>
                </div>
            </div>
        `;
        
        item.addEventListener('click', () => selectArea(area));
        dropdown.appendChild(item);
    });

    dropdown.style.display = 'block';
}

function selectArea(area) {
    selectedArea = area;
    formData.area_id = area.id;
    document.getElementById('areaSearch').value = area.area_name;
    document.getElementById('areaDropdown').style.display = 'none';
    
    // Display selected area
    document.getElementById('selectedAreaDisplay').style.display = 'block';
    document.getElementById('displayAreaName').textContent = area.area_name;
    document.getElementById('displayWard').textContent = area.ward_number;
    document.getElementById('displayZone').textContent = area.zone_name;
    document.getElementById('displayCircle').textContent = area.circle_name;
}

function showAreaDropdown() {
    const searchTerm = document.getElementById('areaSearch').value;
    if (searchTerm.length >= 2) {
        searchAreas();
    }
}

// Step navigation
async function goToStep(step) {
    if (step === 2) {
        // Validate step 1
        if (!validateStep1()) {
            showMessage('step1Message', 'Please fill in all required fields', 'error');
            return;
        }
        // Send OTP
        await sendOTP();
        return;
    } else if (step === 3) {
        // Verify OTP
        await verifyOTP();
        return;
    } else if (step === 4) {
        // Submit complaint
        await submitComplaint();
        return;
    }
    
    currentStep = step;
    updateDisplay();
    updateProgressBar();
    window.scrollTo(0, 0);
}

function validateStep1() {
    return formData.name && formData.phone && formData.email && 
           formData.aadhar && formData.area_id && formData.full_address;
}

// OTP functions
async function sendOTP() {
    try {
        const response = await fetch(`${API_URL}/api/auth/send-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: formData.email })
        });

        if (response.ok) {
            currentStep = 2;
            document.getElementById('otpEmail').textContent = formData.email;
            updateDisplay();
            updateProgressBar();
            window.scrollTo(0, 0);
        } else {
            showMessage('step1Message', 'Error sending OTP', 'error');
        }
    } catch (error) {
        console.error('[v0] Error sending OTP:', error);
        showMessage('step1Message', 'Error: Failed to send OTP', 'error');
    }
}

async function verifyOTP() {
    const otp = document.getElementById('otp').value;
    if (otp.length !== 6) {
        showMessage('step2Message', 'Please enter a valid 6-digit OTP', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/auth/verify-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: formData.email, otp })
        });

        const data = await response.json();
        if (response.ok) {
            currentStep = 3;
            updateDisplay();
            updateProgressBar();
            window.scrollTo(0, 0);
        } else {
            showMessage('step2Message', data.error || 'Invalid OTP', 'error');
        }
    } catch (error) {
        console.error('[v0] Error verifying OTP:', error);
        showMessage('step2Message', 'Error: Failed to verify OTP', 'error');
    }
}

// Complaint submission
async function submitComplaint() {
    if (!formData.description.trim()) {
        showMessage('step3Message', 'Please describe your complaint', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/complaints/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (response.ok) {
            // Display success
            currentStep = 4;
            document.getElementById('successComplaintId').textContent = data.complaint_id;
            document.getElementById('successCategory').textContent = data.category || 'Processing...';
            document.getElementById('successCriticality').textContent = data.criticality || 'Processing...';
            document.getElementById('successZone').textContent = data.zone || (selectedArea?.zone_name || '-');
            document.getElementById('successLocality').textContent = data.locality || (selectedArea?.area_name || '-');
            document.getElementById('successAssignedZone').textContent = data.zone || (selectedArea?.zone_name || '-');
            
            updateDisplay();
            updateProgressBar();
            window.scrollTo(0, 0);
        } else {
            showMessage('step3Message', data.error || 'Error submitting complaint', 'error');
        }
    } catch (error) {
        console.error('[v0] Error submitting complaint:', error);
        showMessage('step3Message', 'Error: Failed to submit complaint', 'error');
    }
}

// Display update
function updateDisplay() {
    // Hide all steps
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step3').style.display = 'none';
    document.getElementById('step4').style.display = 'none';
    
    // Show current step
    document.getElementById(`step${currentStep}`).style.display = 'block';
    document.getElementById('currentStep').textContent = currentStep;
}

function updateProgressBar() {
    for (let i = 1; i <= 4; i++) {
        const progress = document.getElementById(`progress${i}`);
        if (i <= currentStep) {
            progress.className = 'h-2 flex-1 rounded-full transition-colors bg-blue-500';
        } else {
            progress.className = 'h-2 flex-1 rounded-full transition-colors bg-slate-700';
        }
    }
}

// Voice input
function initializeSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        const voiceBtn = document.getElementById('voiceBtn');
        if (voiceBtn) voiceBtn.style.display = 'none';
        console.warn('[v0] Speech Recognition not supported');
        return;
    }

    recognitionRef = new SpeechRecognition();
    recognitionRef.continuous = true;
    recognitionRef.interimResults = true;
    recognitionRef.lang = currentLanguage;

    recognitionRef.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        if (finalTranscript) {
            const textarea = document.getElementById('description');
            textarea.value = textarea.value + finalTranscript;
            formData.description = textarea.value;
        }
    };

    recognitionRef.onerror = (event) => {
        console.error('[v0] Speech recognition error:', event.error);
        const voiceError = document.getElementById('voiceError');
        if (voiceError) {
            voiceError.textContent = 'Voice input error. Please try again.';
            voiceError.style.display = 'block';
        }
        isListening = false;
        updateVoiceButtonState();
    };

    recognitionRef.onend = () => {
        isListening = false;
        updateVoiceButtonState();
    };
}

function toggleVoiceInput() {
    if (!recognitionRef) {
        alert('Voice input not supported in your browser');
        return;
    }

    if (isListening) {
        recognitionRef.stop();
        isListening = false;
    } else {
        recognitionRef.lang = currentLanguage;
        recognitionRef.start();
        isListening = true;
    }
    
    updateVoiceButtonState();
}

function setLanguage(lang) {
    currentLanguage = lang;
    if (isListening) {
        recognitionRef.stop();
        recognitionRef.start();
    }
    
    // Update button styling
    document.getElementById('langEn').className = lang === 'en-IN' ? 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-medium' : 'border-2 border-slate-600 text-slate-300 hover:bg-slate-700 px-4 py-2 rounded font-medium';
    document.getElementById('langHi').className = lang === 'hi-IN' ? 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-medium' : 'border-2 border-slate-600 text-slate-300 hover:bg-slate-700 px-4 py-2 rounded font-medium';
    document.getElementById('langTe').className = lang === 'te-IN' ? 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-medium' : 'border-2 border-slate-600 text-slate-300 hover:bg-slate-700 px-4 py-2 rounded font-medium';
}

function updateVoiceButtonState() {
    const voiceBtn = document.getElementById('voiceBtn');
    const listeningIndicator = document.getElementById('listeningIndicator');
    
    if (isListening) {
        voiceBtn.className = 'bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded font-medium flex items-center gap-2';
        voiceBtn.textContent = '';
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('class', 'w-4 h-4');
        svg.setAttribute('fill', 'currentColor');
        svg.setAttribute('viewBox', '0 0 24 24');
        svg.innerHTML = '<path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm6.3-9c-.44 0-.8.36-.8.8C17.5 7.74 15.9 10 14 10c-.44 0-.8.36-.8.8V11c0 .44.36.8.8.8 2.67 0 5.02-1.94 5.5-4.5v-.7c0-.44-.36-.8-.8-.8z"/>';
        voiceBtn.appendChild(svg);
        voiceBtn.appendChild(document.createTextNode(' Stop Voice Input'));
        listeningIndicator.style.display = 'block';
    } else {
        voiceBtn.className = 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-medium flex items-center gap-2';
        voiceBtn.textContent = '';
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('class', 'w-4 h-4');
        svg.setAttribute('fill', 'currentColor');
        svg.setAttribute('viewBox', '0 0 24 24');
        svg.innerHTML = '<path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm6.3-9c-.44 0-.8.36-.8.8C17.5 7.74 15.9 10 14 10c-.44 0-.8.36-.8.8V11c0 .44.36.8.8.8 2.67 0 5.02-1.94 5.5-4.5v-.7c0-.44-.36-.8-.8-.8z"/>';
        voiceBtn.appendChild(svg);
        voiceBtn.appendChild(document.createTextNode(' Start Voice Input'));
        listeningIndicator.style.display = 'none';
    }
}

function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const className = type === 'error' ? 'bg-red-900-20 border border-red-700 text-red-400' : 'bg-green-900-20 border border-green-700 text-green-400';
    element.className = `${className} p-4 rounded mb-4`;
    element.textContent = message;
    element.style.display = 'block';
}

// Utility function: debounce
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
