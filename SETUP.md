# Story Audio Generator - Setup & Usage

A web application that generates audio narration of a story with a user-provided character name.

## Features

✅ Web-based UI (no terminal knowledge needed)  
✅ Real-time character name replacement  
✅ Natural Hindi speech synthesis using edge-tts & MadhurNeural  
✅ Audio player built into the app  
✅ Download generated audio files  
✅ Responsive, modern design  

## Prerequisites

- Python 3.8+
- The story file at `/workspaces/TTS/input/hindi_story_v2.txt` (already exists)

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** - web framework
- **edge-tts** - Microsoft Text-to-Speech
- Plus all other TTS dependencies

### 2. Run the application

```bash
python app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
```

### 3. Access the web app

In Codespaces:
- Click the "Ports" tab at the bottom
- Look for port 5000
- Click the globe icon or copy the public URL

Or manually navigate to:
```
https://<your-codespace-name>-5000.app.github.dev
```

## How It Works

1. **Enter a character name** (e.g., "Saurabh", "Priya", "Arjun")
2. **Click "Generate Audio"**
3. The app:
   - Reads the story from `input/hindi_story_v2.txt`
   - Replaces all `[NAME]` placeholders with your name
   - Generates audio using Microsoft edge-tts with MadhurNeural (male Hindi voice)
   - Saves the file to `output/` folder
4. **Listen** to the generated audio in the browser player
5. **Download** the MP3 file if you want to keep it

## File Structure

```
/workspaces/TTS/
├── app.py                      # Main Flask application
├── templates/
│   └── index.html             # Web UI
├── input/
│   └── hindi_story_v2.txt     # Story source
├── output/                     # Generated audio files (auto-created)
└── requirements.txt           # Python dependencies
```

## Customization

### Change the voice
Edit `app.py` line 13:
```python
VOICE = "hi-IN-MadhurNeural"  # Male voice
```

Other Hindi voices available:
- `hi-IN-SwaraNeural` - Female voice
- `hi-IN-MadhurNeural` - Male voice

### Use a different story file
Edit `app.py` line 10:
```python
STORY_PATH = Path("/workspaces/TTS/input/hindi_story.txt")  # Change this
```

## Troubleshooting

### Port already in use
If port 5000 is already taken, modify `app.py` last line:
```python
app.run(debug=True, host="0.0.0.0", port=5001)  # Change 5001 to another port
```

### Audio generation is slow
This is normal! Edge-tts generates audio in real-time. A typical story takes 30-120 seconds depending on length.

### File not found error
Make sure:
- `/workspaces/TTS/input/hindi_story_v2.txt` exists
- The file contains `[NAME]` placeholders to replace

## API Endpoints

If you want to integrate with other apps:

### Generate audio (single file)
```
POST /generate
Content-Type: application/json

{
  "name": "Saurabh"
}

Response: {
  "success": true,
  "filename": "story_Saurabh_20260302_143022.mp3",
  "message": "Audio generated successfully for Saurabh!",
  "playlist": ["story_Saurabh_20260302_143022.mp3", ...]  # current files
}
```

### Generate playlist (split story into sections)
```
POST /generate_playlist
Content-Type: application/json

{
  "name": "Saurabh"
}

Response: {
  "success": true,
  "files": ["story_Saurabh_20260302_143022.mp3", "story_Saurabh_20260302_20260302_143030.mp3"],
  "playlist": [...all files...],
  "message": "Generated 3 sections for Saurabh."
}
```

### List available audio files
```
GET /list_audio
```

Returns JSON with all MP3 filenames.

### Download audio
```
GET /download/<filename>
```

Returns the MP3 file as attachment.
