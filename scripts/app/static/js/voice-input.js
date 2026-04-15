/**
 * Voice Input Module
 * Handles Web Speech API integration for voice-to-text conversion
 */

let recognition;
let isListening = false;
let currentLanguage = 'en-IN';

/**
 * Initialize voice input with Web Speech API
 */
function initializeVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (!SpeechRecognition) {
    console.error('[VoiceInput] Speech Recognition not supported');
    disableVoiceButtons();
    return;
  }
  
  recognition = new SpeechRecognition();
  
  // Configuration
  recognition.continuous = true;  // Keep listening
  recognition.interimResults = true;  // Show live results
  recognition.lang = currentLanguage;
  
  // Setup event listeners
  setupRecognitionListeners();
  setupLanguageButtons();
  setupVoiceButton();
}

/**
 * Setup recognition event listeners
 */
function setupRecognitionListeners() {
  recognition.onstart = function() {
    isListening = true;
    updateVoiceUI();
  };
  
  recognition.onresult = function(event) {
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
    
    // Update description field
    if (finalTranscript) {
      const descField = document.getElementById('description');
      if (descField) {
        descField.value += finalTranscript;
      }
    }
    
    // Show interim results
    if (interimTranscript) {
      console.log('[VoiceInput] Interim:', interimTranscript);
    }
  };
  
  recognition.onerror = function(event) {
    console.error('[VoiceInput] Error:', event.error);
    handleVoiceError(event.error);
    isListening = false;
    updateVoiceUI();
  };
  
  recognition.onend = function() {
    isListening = false;
    updateVoiceUI();
  };
}

/**
 * Setup language button listeners
 */
function setupLanguageButtons() {
  const langButtons = document.querySelectorAll('.lang-btn');
  
  langButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      // Stop listening if active
      if (isListening) {
        recognition.stop();
      }
      
      // Update language
      currentLanguage = this.getAttribute('data-lang');
      if (recognition) {
        recognition.lang = currentLanguage;
      }
      
      // Update UI
      langButtons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      // Update current language display
      const langMap = {
        'en-IN': 'English',
        'hi-IN': 'Hindi',
        'te-IN': 'Telugu'
      };
      const currentLangSpan = document.getElementById('currentLang');
      if (currentLangSpan) {
        currentLangSpan.textContent = langMap[currentLanguage];
      }
    });
  });
}

/**
 * Setup voice button listener
 */
function setupVoiceButton() {
  const voiceBtn = document.getElementById('voiceBtn');
  
  if (!voiceBtn) return;
  
  voiceBtn.addEventListener('click', function(e) {
    e.preventDefault();
    
    if (!recognition) {
      console.error('[VoiceInput] Recognition not available');
      return;
    }
    
    if (isListening) {
      recognition.stop();
      isListening = false;
    } else {
      try {
        recognition.lang = currentLanguage;
        recognition.start();
      } catch (error) {
        console.error('[VoiceInput] Error starting recognition:', error);
        handleVoiceError('Failed to start voice input');
      }
    }
    
    updateVoiceUI();
  });
}

/**
 * Update voice UI based on listening state
 */
function updateVoiceUI() {
  const voiceBtn = document.getElementById('voiceBtn');
  const voiceStatus = document.getElementById('voiceStatus');
  const listeningHint = document.getElementById('listeningHint');
  
  if (!voiceBtn) return;
  
  if (isListening) {
    voiceBtn.textContent = '⏹️ Stop Voice Input';
    voiceBtn.classList.add('listening');
    
    if (voiceStatus) {
      voiceStatus.innerHTML = '<span class="pulse-dot"></span> Listening...';
      voiceStatus.style.display = 'flex';
    }
    
    if (listeningHint) {
      listeningHint.style.display = 'block';
    }
  } else {
    voiceBtn.textContent = '🎤 Start Voice Input';
    voiceBtn.classList.remove('listening');
    
    if (voiceStatus) {
      voiceStatus.style.display = 'none';
    }
    
    if (listeningHint) {
      listeningHint.style.display = 'none';
    }
  }
}

/**
 * Handle voice recognition errors
 */
function handleVoiceError(error) {
  const errorAlert = document.getElementById('errorAlert');
  const errorMessage = document.getElementById('errorMessage');
  
  let message = 'Voice input error. Please try again.';
  
  switch (error) {
    case 'no-speech':
      message = 'No speech detected. Please speak clearly and try again.';
      break;
    case 'audio-capture':
      message = 'No microphone found. Please check your device.';
      break;
    case 'not-allowed':
      message = 'Microphone access denied. Please allow microphone permissions.';
      break;
    case 'network':
      message = 'Network error. Please check your connection.';
      break;
  }
  
  if (errorAlert && errorMessage) {
    errorMessage.textContent = message;
    errorAlert.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
      errorAlert.style.display = 'none';
    }, 5000);
  }
  
  console.error('[VoiceInput] Error:', message);
}

/**
 * Disable voice buttons if Speech Recognition not supported
 */
function disableVoiceButtons() {
  const voiceBtn = document.getElementById('voiceBtn');
  const langButtons = document.querySelectorAll('.lang-btn');
  
  if (voiceBtn) {
    voiceBtn.disabled = true;
    voiceBtn.textContent = '🎤 Voice Input Not Supported';
  }
  
  langButtons.forEach(btn => {
    btn.disabled = true;
  });
  
  handleVoiceError('Speech Recognition not supported in this browser');
}

/**
 * Stop listening
 */
function stopListening() {
  if (recognition && isListening) {
    recognition.stop();
  }
}

/**
 * Start listening
 */
function startListening() {
  if (recognition && !isListening) {
    try {
      recognition.lang = currentLanguage;
      recognition.start();
    } catch (error) {
      console.error('[VoiceInput] Error starting:', error);
    }
  }
}

/**
 * Get transcribed text
 */
function getTranscribedText() {
  const descField = document.getElementById('description');
  return descField ? descField.value : '';
}

/**
 * Clear transcribed text
 */
function clearTranscribedText() {
  const descField = document.getElementById('description');
  if (descField) {
    descField.value = '';
  }
}

/**
 * Export for use in other modules
 */
const VoiceInput = {
  initializeVoiceInput,
  stopListening,
  startListening,
  getTranscribedText,
  clearTranscribedText,
  isListening: () => isListening,
};
