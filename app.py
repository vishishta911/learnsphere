"""
═════════════════════════════════════════════════════════════════════
LearnSphere - AI-Powered Learning Platform Backend
═════════════════════════════════════════════════════════════════════

A Flask web application that generates Machine Learning educational
content in multiple formats (text, code, audio, visual) using OpenRouter
free models.

Features:
- Generate tailored ML explanations for different learning levels
- Create Python code examples with detailed comments
- Convert explanations to MP3 audio files
- Generate prompts for ML architecture diagrams
- Uses free models via OpenRouter API

Author: LearnSphere Team
Date: February 2026
═════════════════════════════════════════════════════════════════════
"""

# ═════════════════════════════════════════════════════════════════════
# IMPORTS & INITIALIZATION
# ═════════════════════════════════════════════════════════════════════

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import requests
from gtts import gTTS
from datetime import datetime
import uuid
import time


# Load environment variables from .env file
# This keeps sensitive information (API keys) out of the code
load_dotenv()

# Create Flask application instance
app = Flask(__name__)


# ═════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════

# Get OpenRouter API key from environment variables (NOT hardcoded!)
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Primary model with automatic fallbacks for reliability
# OpenRouter's auto-routing intelligently selects the best available model
OPENROUTER_MODELS = [
    "openrouter/auto",  # Primary: Auto-routing to best available model
    "meta-llama/llama-2-7b-chat",  # Fallback 1: Reliable Llama 2
    "mistralai/mistral-7b-instruct",  # Fallback 2: Mistral (no :free suffix)
]
OPENROUTER_MODEL = OPENROUTER_MODELS[0]  # Start with auto-routing

# Configure the OpenRouter API with the API key
if OPENROUTER_API_KEY:
    print("✓ OpenRouter API configured successfully")
    print(f"  Primary model: {OPENROUTER_MODEL}")
    print(f"  Fallback models available: {OPENROUTER_MODELS[1]}, {OPENROUTER_MODELS[2]}")
else:
    print("⚠ Warning: OPENROUTER_API_KEY not found in .env file")
    print("ℹ Get a free API key at: https://openrouter.ai")
    print("ℹ Content generation will not work without the API key")


# ═════════════════════════════════════════════════════════════════════
# OPENROUTER API HELPER
# ═════════════════════════════════════════════════════════════════════

def call_openrouter_api(prompt):
    """
    Make a request to OpenRouter API for content generation with intelligent fallback system.
    
    Features:
    - Tries primary model (auto-routing) first
    - Automatically falls back to alternative models if primary fails
    - Retries on rate limits (429) with exponential backoff
    - Handles timeouts and connection errors gracefully
    
    Args:
        prompt (str): The prompt to send to the model
    
    Returns:
        str: The generated response text
    
    Raises:
        Exception: If all models fail or API key not configured
    """
    
    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY not configured. Add it to your .env file")
    
    # Try each model in the fallback list
    for model_index, model_name in enumerate(OPENROUTER_MODELS):
        print(f"\n  📍 Attempting with model: {model_name}")
        
        # Retry configuration for each model: exponential backoff with max 3 retries
        max_retries = 3
        base_delay = 2  # Start with 2 second delay
        
        for attempt in range(max_retries + 1):
            try:
                # Prepare request headers with API key
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "http://localhost:5000",
                    "X-Title": "LearnSphere",
                    "Content-Type": "application/json"
                }
                
                # Prepare request payload
                data = {
                    "model": model_name,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,  # Balanced creativity and consistency
                    "max_tokens": 2000   # Limit response length for faster generation
                }
                
                # Make API request
                if attempt == 0:
                    print(f"     Calling OpenRouter API...")
                else:
                    print(f"     Retry attempt {attempt}...")
                    
                response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result['choices'][0]['message']['content']
                    print(f"     ✓ Success with {model_name}")
                    return generated_text
                
                # Handle model not found - try next fallback
                elif response.status_code == 404:
                    error_text = response.text
                    if "No endpoints found" in error_text or "model" in error_text.lower():
                        print(f"     ✗ Model '{model_name}' not available, trying next fallback...")
                        break  # Break inner loop to try next model
                    else:
                        raise Exception(f"API Error 404: {error_text}")
                
                # Handle rate limiting with automatic retry
                elif response.status_code == 429:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt)
                        print(f"     ⏳ Rate limited. Waiting {delay}s before retry...")
                        time.sleep(delay)
                        continue  # Retry current model
                    else:
                        # Exhausted retries for this model, try next
                        print(f"     ⏳ Rate limited after {max_retries} retries. Trying next fallback...")
                        break  # Break inner loop to try next model
                
                # Handle other API errors
                else:
                    raise Exception(f"OpenRouter API error {response.status_code}: {response.text}")
                
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    print(f"     ⏳ Timeout. Waiting {delay}s before retry...")
                    time.sleep(delay)
                    continue
                else:
                    print(f"     ✗ Timeout after {max_retries} retries on {model_name}. Trying next fallback...")
                    break
                    
            except requests.exceptions.ConnectionError:
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    print(f"     ⏳ Connection error. Waiting {delay}s before retry...")
                    time.sleep(delay)
                    continue
                else:
                    print(f"     ✗ Connection error on {model_name}. Trying next fallback...")
                    break
                    
            except Exception as e:
                error_msg = str(e)
                # If API key is invalid, no point trying other models
                if "unauthorized" in error_msg.lower() or "invalid" in error_msg.lower():
                    raise Exception(f"OpenRouter API authentication failed: {error_msg}")
                # Otherwise, move to next model
                print(f"     ✗ Error with {model_name}: {error_msg}. Trying next fallback...")
                break
        
        # If we've tried all models, check if this was the last one
        if model_index == len(OPENROUTER_MODELS) - 1:
            # This was the last model, all failed
            raise Exception(
                f"All models failed. Please verify your API key and check OpenRouter status. "
                f"Attempted models: {', '.join(OPENROUTER_MODELS)}"
            )
    
    # Fallback error (shouldn't reach here)
    raise Exception("Failed to generate content. Please try again.")


# ═════════════════════════════════════════════════════════════════════
# CONTENT GENERATION FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

def generate_text_content(topic, depth):
    """
    Generate a structured text explanation for a Machine Learning topic.
    
    Args:
        topic (str): The ML topic to explain (e.g., "Neural Networks")
        depth (str): Learning level - 'beginner', 'intermediate', 'advanced'
    
    Returns:
        str: A formatted explanation with structure and examples
    
    Example:
        >>> text = generate_text_content("Decision Trees", "beginner")
        >>> print(text[:100])  # Print first 100 characters
    """
    
    # Create a prompt that guides the model to generate structured content
    prompt = f"""Please provide a comprehensive {depth} level explanation about: {topic}

Structure your response exactly as follows:
1. Definition/Overview - Clear, simple introduction
2. Key Concepts - 3-4 main concepts with brief explanations
3. Practical Examples - Real-world applications or code examples
4. Conclusion - Summary and next steps for learning

Use clear, simple language suitable for a {depth} level learner.
Be concise and focus on the most important concepts."""
    
    try:
        # Call OpenRouter API to generate content
        response_text = call_openrouter_api(prompt)
        return response_text
    except Exception as e:
        raise Exception(f"Failed to generate text content: {str(e)}")


def generate_code_content(topic, depth):
    """
    Generate beginner-friendly Python code demonstrating a concept.
    
    Args:
        topic (str): The ML topic to demonstrate with code
        depth (str): Learning level - 'beginner', 'intermediate', 'advanced'
    
    Returns:
        str: Python code with detailed comments explaining each line
    """
    
    # Create a prompt that guides code generation with proper structure
    prompt = f"""Generate {depth} level Python code to demonstrate: {topic}

Requirements:
1. Add detailed comments explaining EVERY section
2. Use popular ML libraries (scikit-learn, pandas, numpy)
3. Include a simple example that can be run immediately
4. Adjust code complexity for {depth} level learners
5. Use clear variable names and follow Python best practices
6. Include explanatory comments before each major section

Format: Pure Python code that learners can understand and run."""
    
    try:
        response_text = call_openrouter_api(prompt)
        return response_text
    except Exception as e:
        raise Exception(f"Failed to generate code content: {str(e)}")


def generate_audio_content(topic, depth):
    """
    Generate a text explanation and convert it to audio (MP3).
    
    Args:
        topic (str): The ML topic to create audio for
        depth (str): Learning level - 'beginner', 'intermediate', 'advanced'
    
    Returns:
        dict: Contains 'text' content, 'audio_file' path, and 'filename'
    
    Notes:
        - Audio files are saved in static/audio/ directory
        - Each file has a unique ID and timestamp to prevent overwrites
        - Text is limited to 5000 characters for stability
    """
    
    try:
        # First, generate the text explanation
        text_content = generate_text_content(topic, depth)
        
        # Create audio directory if it doesn't exist
        # Uses absolute path for reliability
        audio_dir = os.path.join(app.static_folder, 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        # Generate unique filename using UUID + timestamp
        # This prevents files from being overwritten
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_id = str(uuid.uuid4())[:8]  # First 8 characters of UUID
        filename = f"explanation_{file_id}_{timestamp}.mp3"
        filepath = os.path.join(audio_dir, filename)
        
        # Limit text length to prevent API timeouts (5000 chars max)
        text_to_speak = text_content[:5000]
        
        # Convert text to speech using Google Text-to-Speech (gTTS)
        print(f"  Converting text to speech ({len(text_to_speak)} characters)...")
        tts = gTTS(text=text_to_speak, lang='en', slow=False)
        tts.save(filepath)
        
        # Verify the file was created successfully
        if not os.path.exists(filepath):
            raise Exception("Audio file creation failed")
        
        print(f"  ✓ Audio saved: {filename}")
        
        return {
            'text': text_content,
            'audio_file': f'/static/audio/{filename}',
            'filename': filename
        }
    except Exception as e:
        raise Exception(f"Failed to generate audio content: {str(e)}")


def generate_visual_content(topic, depth):
    """
    Generate a detailed prompt for creating ML architecture diagrams.
    
    Args:
        topic (str): The ML topic to visualize
        depth (str): Learning level - 'beginner', 'intermediate', 'advanced'
    
    Returns:
        str: A prompt suitable for diagram tools (Mermaid, draw.io, etc.)
    """
    
    # Create a prompt that generates visualization instructions
    prompt = f"""Generate a detailed visualization prompt for: {topic}

The prompt should describe:
1. Overall architecture or workflow
2. Key components and their relationships
3. Data flow between components
4. Suggested visual elements (shapes, arrows, colors)
5. Be suitable for {depth} level learners
6. Be compatible with Mermaid or draw.io tools

Format as clear, step-by-step visualization instructions."""
    
    try:
        response_text = call_openrouter_api(prompt)
        return response_text
    except Exception as e:
        raise Exception(f"Failed to generate visual content: {str(e)}")


# ═════════════════════════════════════════════════════════════════════
# ROUTE HANDLERS
# ═════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    """
    Serve the main homepage.
    
    Returns:
        HTML: The index.html template rendered with Flask
    """
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    Main API endpoint for generating learning content.
    
    This endpoint accepts a POST request with JSON data and generates
    content based on the requested mode. It handles all validation,
    error checking, and calls the appropriate generation function.
    
    Expected JSON Input:
    {
        "topic": "string - ML topic to learn about",
        "depth": "string - 'beginner', 'intermediate', or 'advanced'",
        "mode": "string - 'text', 'code', 'audio', or 'visual'"
    }
    
    Response JSON (Success):
    {
        "success": true,
        "content": "generated content or explanation",
        "topic": "provided topic",
        "depth": "provided depth level",
        "mode": "provided mode"
    }
    
    Response JSON (Error):
    {
        "success": false,
        "error": "error message description",
        "error_type": "exception type"
    }
    
    HTTP Status Codes:
    - 200: Content generated successfully
    - 400: Invalid input (missing topic, invalid depth/mode)
    - 500: Server error (API failure, file system error)
    """
    
    try:
        # ─────────────────────────────────────────────────────────────
        # Step 1: Get and validate request data
        # ─────────────────────────────────────────────────────────────
        
        data = request.get_json()
        
        # Check if JSON data was provided
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Extract and clean the input parameters
        topic = data.get('topic', '').strip()
        depth = data.get('depth', 'beginner').lower()
        mode = data.get('mode', 'text').lower()
        
        # ─────────────────────────────────────────────────────────────
        # Step 2: Validate required fields
        # ─────────────────────────────────────────────────────────────
        
        # Topic is mandatory
        if not topic:
            return jsonify({
                'success': False,
                'error': 'Topic is required'
            }), 400
        
        # Validate and correct depth if invalid
        valid_depths = ['beginner', 'intermediate', 'advanced']
        if depth not in valid_depths:
            depth = 'beginner'  # Default to beginner
        
        # Validate and correct mode if invalid
        valid_modes = ['text', 'code', 'audio', 'visual']
        if mode not in valid_modes:
            mode = 'text'  # Default to text
        
        print(f"\n📚 Generating {mode} content...")
        print(f"   Topic: {topic}")
        print(f"   Level: {depth}")
        
        # ─────────────────────────────────────────────────────────────
        # Step 3: Generate content based on requested mode
        # ─────────────────────────────────────────────────────────────
        
        if mode == 'text':
            # Generate text explanation
            content = generate_text_content(topic, depth)
            return jsonify({
                'success': True,
                'content': content,
                'topic': topic,
                'depth': depth,
                'mode': mode
            })
        
        elif mode == 'code':
            # Generate Python code with comments
            content = generate_code_content(topic, depth)
            return jsonify({
                'success': True,
                'content': content,
                'topic': topic,
                'depth': depth,
                'mode': mode
            })
        
        elif mode == 'audio':
            # Generate text + audio
            audio_data = generate_audio_content(topic, depth)
            return jsonify({
                'success': True,
                'text_content': audio_data['text'],
                'audio_file': audio_data['audio_file'],
                'filename': audio_data['filename'],
                'topic': topic,
                'depth': depth,
                'mode': mode,
                'message': 'Audio file generated successfully'
            })
        
        elif mode == 'visual':
            # Generate visualization prompt
            content = generate_visual_content(topic, depth)
            return jsonify({
                'success': True,
                'content': content,
                'topic': topic,
                'depth': depth,
                'mode': mode,
                'message': 'Use this prompt with Mermaid or draw.io'
            })
    
    except Exception as e:
        # Handle any unexpected errors gracefully
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500


@app.route('/audio/<filename>')
def serve_audio(filename):
    """
    Serve audio files from the static/audio directory.
    
    This endpoint allows the frontend to download audio files with
    the correct MIME type for playback in browsers.
    
    Args:
        filename (str): Name of the audio file to serve
    
    Security:
        - Validates filename to prevent directory traversal attacks
        - Only serves files from the static/audio directory
    
    Returns:
        Audio file (MP3) with proper MIME type
    
    HTTP Status Codes:
        - 200: File served successfully
        - 400: Invalid filename
        - 404: File not found
        - 500: Server error
    """
    
    # Prevent directory traversal attacks
    # Reject filenames containing ".." or starting with "/"
    if '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Invalid filename'}), 400
    
    # Get the audio directory
    audio_dir = os.path.join(app.static_folder, 'audio')
    filepath = os.path.join(audio_dir, filename)
    
    # Check if file exists before trying to serve it
    if not os.path.exists(filepath):
        return jsonify({'error': 'Audio file not found'}), 404
    
    try:
        # Serve the file with correct MIME type for audio
        return send_from_directory(
            audio_dir,
            filename,
            mimetype='audio/mpeg'  # MP3 format MIME type
        )
    except Exception as e:
        return jsonify({'error': f'Error serving audio: {str(e)}'}), 500


# ═════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    """Handle 404 (Page Not Found) errors."""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 (Internal Server Error) errors."""
    return jsonify({'error': 'Internal server error'}), 500


# ═════════════════════════════════════════════════════════════════════
# APPLICATION ENTRY POINT
# ═════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    """
    Run the Flask development server.
    
    Configuration:
    - debug=True: Enable hot reload and detailed error messages
    - host='0.0.0.0': Accept connections from any network interface
    - port=5000: Listen on port 5000
    
    WARNING: In production, use a WSGI server like Gunicorn instead
    """
    print("\n" + "="*60)
    print("LearnSphere - AI Learning Platform")
    print("="*60)
    print("\n🚀 Starting server...")
    print("📍 Interface: http://0.0.0.0:5000")
    print("📍 Local: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
