/*
═════════════════════════════════════════════════════════════════════
LearnSphere - Frontend JavaScript
═════════════════════════════════════════════════════════════════════
Main interactivity logic for the LearnSphere application. This file
handles:
- Form submission and input validation
- API communication with backend (/generate endpoint)
- Dynamic content display based on generation mode
- User interactions (copy, download, etc.)
- UI state management and error handling

Key Functions:
- handleFormSubmit() - Main form handler
- generateContent() - API communication
- displayContent() - Render generated content
- copyToClipboard() - User utility features

═════════════════════════════════════════════════════════════════════
*/

/*
═════════════════════════════════════════════════════════════════════
DOM ELEMENTS - Reference all HTML elements needed by JavaScript
═════════════════════════════════════════════════════════════════════
*/

// Form elements
const generateForm = document.getElementById('generateForm');
const topicInput = document.getElementById('topic');
const depthSelect = document.getElementById('depth');
const modeSelect = document.getElementById('mode');
const generateBtn = document.getElementById('generateBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');

// Output display containers
const errorMessage = document.getElementById('errorMessage');
const loadingState = document.getElementById('loadingState');
const contentDisplay = document.getElementById('contentDisplay');
const emptyState = document.getElementById('emptyState');

// Content type boxes (shown/hidden based on mode)
const textContent = document.getElementById('textContent');
const codeContent = document.getElementById('codeContent');
const audioContent = document.getElementById('audioContent');
const visualContent = document.getElementById('visualContent');

// Content output areas where generated content is displayed
const textOutput = document.getElementById('textOutput');
const codeOutput = document.getElementById('codeOutput');
const audioPlayer = document.getElementById('audioPlayer');
const audioText = document.getElementById('audioText');
const visualOutput = document.getElementById('visualOutput');
const visualMessage = document.getElementById('visualMessage');

// Metadata tag elements
const topicTag = document.getElementById('topicTag');
const depthTag = document.getElementById('depthTag');
const modeTag = document.getElementById('modeTag');


/*
═════════════════════════════════════════════════════════════════════
EVENT LISTENERS - Register interactive user actions
═════════════════════════════════════════════════════════════════════
*/

// Form submission - main entry point
generateForm.addEventListener('submit', handleFormSubmit);

// Copy and download buttons
document.getElementById('copyCodeBtn').addEventListener('click', copyCode);
document.getElementById('downloadAudioBtn').addEventListener('click', downloadAudio);
document.getElementById('copyOutputBtn').addEventListener('click', copyOutput);


/*
═════════════════════════════════════════════════════════════════════
MAIN HANDLER - Form submission logic
═════════════════════════════════════════════════════════════════════
*/

async function handleFormSubmit(event) {
    /**
     * Handle form submission - main entry point for content generation
     * 
     * Flow:
     * 1. Prevent default form submission
     * 2. Get and validate user inputs
     * 3. Disable form and show loading state
     * 4. Call backend API
     * 5. Display returned content
     * 6. Handle any errors gracefully
     */
    
    event.preventDefault();  // Prevent page reload

    // Extract user inputs from form
    const topic = topicInput.value.trim();
    const depth = depthSelect.value;
    const mode = modeSelect.value;

    // Basic client-side validation
    if (!topic) {
        showError('Please enter a topic');
        return;
    }

    // Update UI to show we're working
    disableForm();
    showLoading();
    hideError();

    try {
        // Send request to backend and get response
        const response = await generateContent(topic, depth, mode);

        // Display the generated content
        displayContent(response, mode);
        hideLoading();
        showContentDisplay();

    } catch (error) {
        // Show error message to user
        console.error('Error:', error);
        showError(error.message || 'An error occurred. Please try again.');
        hideLoading();
        
    } finally {
        // Always re-enable form, even if there was an error
        enableForm();
    }
}


/*
═════════════════════════════════════════════════════════════════════
API COMMUNICATION - Fetch API for backend integration
═════════════════════════════════════════════════════════════════════
*/

async function generateContent(topic, depth, mode) {
    /**
     * Send POST request to backend /generate endpoint
     * 
     * Args:
     *   topic (string): ML topic to generate content about
     *   depth (string): Learning level (beginner/intermediate/advanced)
     *   mode (string): Content type (text/code/audio/visual)
     * 
     * Returns:
     *   Promise<Object>: Parsed JSON response with generated content
     * 
     * Throws:
     *   Error: Network or API error
     */
    
    // Prepare request payload
    const requestData = {
        topic: topic,
        depth: depth,
        mode: mode
    };

    try {
        // Make POST request to backend
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        // Parse JSON response
        const data = await response.json();

        // Check for successful response
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Failed to generate content');
        }

        return data;

    } catch (error) {
        throw new Error(`API Error: ${error.message}`);
    }
}


/*
═════════════════════════════════════════════════════════════════════
CONTENT DISPLAY - Render generated content in appropriate format
═════════════════════════════════════════════════════════════════════
*/

function displayContent(response, mode) {
    /**
     * Display content based on requested mode
     * 
     * Updates metadata tags and shows the appropriate content box
     * based on whether user requested text/code/audio/visual content
     */

    // Update metadata tags with request details
    updateMetaTags(response.topic, response.depth, response.mode);

    // Hide all content containers (only show one)
    hideAllContentBoxes();

    // Display content based on mode
    switch (mode) {
        case 'text':
            displayTextContent(response.content);
            break;

        case 'code':
            displayCodeContent(response.content);
            break;

        case 'audio':
            displayAudioContent(response);
            break;

        case 'visual':
            displayVisualContent(response);
            break;

        default:
            showError('Unknown content mode');
    }
}

function displayTextContent(content) {
    /**
     * Display text explanation
     */
    textOutput.innerHTML = formatText(content);
    textContent.style.display = 'block';
}

function displayCodeContent(content) {
    /**
     * Display Python code with syntax highlighting
     */
    codeOutput.textContent = content;
    codeContent.style.display = 'block';

    // Optional: Apply syntax highlighting if using a library like Highlight.js
    // hljs.highlightBlock(codeOutput);
}

function displayAudioContent(response) {
    /**
     * Display audio explanation with player
     * Ensures proper audio file loading and playback
     */
    // Display text explanation
    audioText.innerHTML = formatText(response.text_content);

    // Set audio source - use the path returned from backend
    const audioSource = response.audio_file;
    audioPlayer.src = audioSource;
    
    // Reset audio player
    audioPlayer.currentTime = 0;
    audioPlayer.style.display = 'block';

    // Store audio file info for download
    audioPlayer.dataset.audioFile = audioSource;
    audioPlayer.dataset.filename = response.filename || 'learnsphere_audio.mp3';
    
    // Handle audio loading
    audioPlayer.addEventListener('loadstart', () => {
        console.log('Loading audio from:', audioSource);
    }, { once: true });
    
    // Handle audio loading errors
    audioPlayer.addEventListener('error', () => {
        console.error('Audio loading error:', audioPlayer.error);
        showError('Failed to load audio file. Please try generating again.');
    }, { once: true });
    
    // Handle successful audio load
    audioPlayer.addEventListener('canplay', () => {
        console.log('Audio loaded successfully');
    }, { once: true });

    audioContent.style.display = 'block';
}

function displayVisualContent(response) {
    /**
     * Display visualization prompt
     */
    visualMessage.innerHTML = formatText(response.content);
    visualOutput.textContent = formatText(response.message || '');
    visualContent.style.display = 'block';
}

function updateMetaTags(topic, depth, mode) {
    /**
     * Update and display metadata tags
     */
    topicTag.innerHTML = `<strong>Topic:</strong> ${escapeHtml(topic)}`;
    depthTag.innerHTML = `<strong>Level:</strong> ${capitalize(depth)}`;
    modeTag.innerHTML = `<strong>Mode:</strong> ${capitalize(mode)}`;
}

function hideAllContentBoxes() {
    /**
     * Hide all content display containers
     */
    textContent.style.display = 'none';
    codeContent.style.display = 'none';
    audioContent.style.display = 'none';
    visualContent.style.display = 'none';
}

// ===========================
// UTILITY & HELPER FUNCTIONS
// ===========================

function formatText(text) {
    /**
     * Format text for display
     * Convert line breaks to <br> tags for readability
     */
    if (!text) return '';
    return text
        .trim()
        .split('\n')
        .map(line => escapeHtml(line.trim()))
        .filter(line => line.length > 0)
        .join('<br>');
}

function escapeHtml(text) {
    /**
     * Escape HTML special characters to prevent XSS
     */
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, char => map[char]);
}

function capitalize(text) {
    /**
     * Capitalize first letter of string
     */
    return text.charAt(0).toUpperCase() + text.slice(1);
}

// ===========================
// COPY & DOWNLOAD FUNCTIONS
// ===========================

function copyCode() {
    /**
     * Copy code to clipboard
     */
    const codeText = codeOutput.textContent;
    copyToClipboard(codeText, 'Code copied to clipboard!');
}

function copyOutput() {
    /**
     * Copy all displayed content to clipboard
     */
    let outputText = '';

    // Collect visible content
    if (textOutput.textContent) {
        outputText += 'TEXT EXPLANATION:\n' + textOutput.textContent + '\n\n';
    }
    if (codeOutput.textContent) {
        outputText += 'CODE:\n' + codeOutput.textContent + '\n\n';
    }
    if (audioText.textContent) {
        outputText += 'AUDIO TRANSCRIPT:\n' + audioText.textContent + '\n\n';
    }
    if (visualOutput.textContent) {
        outputText += 'VISUALIZATION:\n' + visualOutput.textContent + '\n\n';
    }

    if (outputText) {
        copyToClipboard(outputText, 'Content copied to clipboard!');
    }
}

function downloadAudio() {
    /**
     * Download audio file
     * Uses filename from response if available
     */
    const audioFile = audioPlayer.dataset.audioFile;
    const filename = audioPlayer.dataset.filename || 'learnsphere_audio.mp3';
    
    if (!audioFile) {
        showError('Audio file not available');
        return;
    }

    try {
        // Create temporary link and trigger download
        const link = document.createElement('a');
        link.href = audioFile;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        showSuccess('Audio download started!');
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download audio file');
    }
}

function copyToClipboard(text, successMessage) {
    /**
     * Copy text to clipboard using modern API
     */
    navigator.clipboard.writeText(text).then(() => {
        showSuccess(successMessage);
    }).catch(err => {
        console.error('Failed to copy:', err);
        showError('Failed to copy to clipboard');
    });
}

function showSuccess(message) {
    /**
     * Show success notification
     */
    const alert = document.createElement('div');
    alert.className = 'alert alert-success';
    alert.textContent = message;
    document.querySelector('.output-section').insertBefore(alert, contentDisplay);

    // Auto-remove after 3 seconds
    setTimeout(() => alert.remove(), 3000);
}

// ===========================
// UI STATE MANAGEMENT
// ===========================

function showLoading() {
    /**
     * Show loading state
     */
    loadingState.style.display = 'block';
    contentDisplay.style.display = 'none';
    emptyState.style.display = 'none';
}

function hideLoading() {
    /**
     * Hide loading state
     */
    loadingState.style.display = 'none';
}

function showContentDisplay() {
    /**
     * Show content display area
     */
    contentDisplay.style.display = 'block';
    emptyState.style.display = 'none';
}

function showError(message) {
    /**
     * Display error message
     */
    errorMessage.textContent = '❌ ' + message;
    errorMessage.style.display = 'block';
}

function hideError() {
    /**
     * Hide error message
     */
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
}

function disableForm() {
    /**
     * Disable form inputs and button
     */
    topicInput.disabled = true;
    depthSelect.disabled = true;
    modeSelect.disabled = true;
    generateBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
}

function enableForm() {
    /**
     * Enable form inputs and button
     */
    topicInput.disabled = false;
    depthSelect.disabled = false;
    modeSelect.disabled = false;
    generateBtn.disabled = false;
    btnText.style.display = 'inline';
    btnLoader.style.display = 'none';
}

// ===========================
// INITIALIZATION
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    /**
     * Initialize on page load
     */
    console.log('LearnSphere initialized!');
    // Form is ready, show empty state
    emptyState.style.display = 'block';
});
