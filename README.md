# LearnSphere 🎓

An AI-powered learning platform that generates Machine Learning explanations in multiple formats using **OpenRouter free models**.

## Features

- **Text Explanations** - Comprehensive ML topic explanations tailored to your level
- **Code Generation** - Beginner-friendly Python ML code with detailed comments
- **Audio Explanations** - Text-to-speech conversion of explanations (MP3 format)
- **Visual Prompts** - Prompts for creating ML workflow diagrams
- **Multiple Learning Levels** - Beginner, Intermediate, Advanced
- **Powerful Free Model** - Uses Google Gemma 3.27B (free from OpenRouter!)

## Tech Stack

- **Backend**: Flask (Python web framework)
- **AI**: OpenRouter API with Google Gemma 3.27B model
- **Text-to-Speech**: gTTS for audio conversion
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Audio**: MP3 files served via Flask

## Project Structure

```
learnsphere/
├── app.py                 # Flask backend with OpenRouter integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── templates/
│   └── index.html        # Main frontend page
└── static/
    ├── css/
    │   └── style.css     # Modern styling
    ├── js/
    │   └── main.js       # Frontend interactions
    └── audio/            # Generated audio files (auto-created)
```

## Installation & Setup

### 1. Get OpenRouter API Key (FREE!)

1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up with email or GitHub (no credit card required!)
3. Go to your API keys section
4. Create a new API key
5. Copy the key (format: `sk-or-v1-...`)

**Default Model: Google Gemma 3.27B** ⭐
- High quality responses
- Fast generation (5-10 seconds)
- Excellent for code and explanations
- Completely free!

**Alternative Free Models Available:**
- Llama 2 7B - Reliable, slightly slower
- OpenChat 7B - Fast and good quality
- Mistral 7B - Better reasoning

### 2. Clone/Download the Project

```bash
cd learnsphere
```

### 3. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables

```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env and add your OpenRouter API key
OPENROUTER_API_KEY=sk_your_key_here_sk
```

### 6. Create Audio Directory

```bash
mkdir static/audio
```

### 7. Run the Application

```bash
python app.py
```

The app will be available at: `http://localhost:5000`

## Usage

1. **Enter a Topic** - Type an ML topic (e.g., "Neural Networks")
2. **Select Level** - Choose your learning level (Beginner/Intermediate/Advanced)
3. **Choose Mode**:
   - **Text**: Read comprehensive explanation
   - **Code**: Get Python ML code with comments
   - **Audio**: Listen to explanation (MP3)
   - **Visual**: Get diagram creation prompt
4. **Click Generate** - Wait for AI to generate content
5. **View/Download** - Read, listen, or download the content

## Audio Features

- **Automatic Generation**: Text-to-speech conversion using gTTS
- **Unique Files**: Each audio file has a unique ID and timestamp
- **Easy Download**: Download generated audio files directly
- **Playback**: Built-in audio player with controls

## API Endpoints

### POST `/generate`

Generate learning content

**Request:**
```json
{
  "topic": "Decision Trees",
  "depth": "beginner",
  "mode": "code"
}
```

**Response:**
```json
{
  "success": true,
  "content": "def decision_tree():\n  ...",
  "topic": "Decision Trees",
  "depth": "beginner",
  "mode": "code"
}
```

**Modes:**
- `text` - Text explanation
- `code` - Python code
- `audio` - Audio explanation + transcript
- `visual` - Visualization prompt

**Depths:**
- `beginner`
- `intermediate`
- `advanced`

## File Organization

### Backend Features

- **generate_text_content()** - Creates structured explanations
- **generate_code_content()** - Generates clean Python code
- **generate_audio_content()** - Converts text to MP3
- **generate_visual_content()** - Creates diagram prompts
- **serve_audio()** - Properly serves audio files with MIME types

### Frontend Features

- **Form Validation** - Ensures required inputs
- **Loading States** - Shows spinner during generation
- **Error Handling** - User-friendly error messages
- **Content Display** - Dynamic rendering based on mode
- **Copy/Download** - Easy content sharing

## Error Handling

The application includes robust error handling:

- **Input Validation** - Validates topic, depth, and mode
- **API Errors** - Graceful handling of API failures
- **Audio Errors** - Checks for successful file creation
- **File Errors** - Validates file existence and accessibility
- **Network Errors** - Handles fetch failures

## Troubleshooting

### Audio files not playing
- Check that `/static/audio` directory exists
- Verify files are being created in the correct location
- Check browser console for load errors

### API returns errors
- Verify OPENROUTER_API_KEY is correct in .env
- Check internet connection at https://openrouter.ai
- Make sure your free tier quota hasn't been exceeded
- Try with a different free model if one is slow

### Form not submitting
- Check browser console for JavaScript errors
- Verify Flask server is running
- Ensure topic field is not empty
- Check that OpenRouter API key is valid

## Browser Compatibility

- Chrome/Chromium - Full support
- Firefox - Full support
- Safari - Full support
- Edge - Full support

## Performance Tips

- Text explanations load fastest
- Code generation takes 2-5 seconds
- Audio generation takes 5-15 seconds (depends on text length)
- Visual prompts generate in 3-8 seconds

## Future Enhancements

- [ ] User accounts and saved content
- [ ] Syntax highlighting for code
- [ ] Batch content generation
- [ ] Export to PDF
- [ ] Interactive quizzes
- [ ] Code execution environment
- [ ] Dark mode toggle

## License

This project is created for educational purposes.

## Support

For issues or questions:
1. Check this README
2. Review your .env configuration
3. Check browser console for errors
4. Verify API key is valid

---

**Made with ❤️ for learners** | Powered by OpenRouter with Free Models
