from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path
import asyncio
import edge_tts
from datetime import datetime

app = Flask(__name__)

# Configuration
STORY_PATH = Path("/workspaces/TTS/input/hindi_story_v2.txt")
OUTPUT_DIR = Path("/workspaces/TTS/output")
OUTPUT_DIR.mkdir(exist_ok=True)
# delimiter used to split story into sections
SECTION_DELIMITER = "\n\n"  # two newlines separate paragraphs
VOICE = "hi-IN-MadhurNeural"  # Male voice in Hindi

def read_story():
    """Read the base story from file"""
    if not STORY_PATH.exists():
        raise FileNotFoundError(f"Story file not found at {STORY_PATH}")
    return STORY_PATH.read_text(encoding="utf-8")


def split_story(text: str) -> list[str]:
    """Split story text into sections based on delimiter."""
    # trim whitespace and ignore empty parts
    parts = [part.strip() for part in text.split(SECTION_DELIMITER) if part.strip()]
    return parts

async def generate_audio(text, character_name):
    """Generate audio from text using edge_tts"""
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_name = "".join(c if c.isalnum() else "_" for c in character_name)
    output_file = OUTPUT_DIR / f"story_{safe_name}_{timestamp}.mp3"
    
    # Voice parameters for more realistic, human-like tone
    # rate: slower speech (-8%) for better comprehension and natural pacing
    # pitch: natural male voice (+0 Hz)
    # volume: slightly dynamic for natural sound (-5%)
    communicate = edge_tts.Communicate(
        text, 
        VOICE,
        rate="-8%",      # Slower, more conversational pace
        pitch="+0Hz",    # Natural pitch
        volume="-5%"     # Slightly softer, more intimate tone
    )
    await communicate.save(str(output_file))
    
    return output_file


def list_audio_files() -> list[str]:
    """Return sorted list of MP3 filenames in the output directory."""
    files = [f.name for f in OUTPUT_DIR.glob("*.mp3")]
    # sort by name which contains timestamp
    return sorted(files)

@app.route("/")
def index():
    """Home page"""
    return render_template("index.html")

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Server is running"}), 200

@app.route("/generate", methods=["POST"])
def generate():
    """Generate audio for the story with user-provided character name"""
    try:
        data = request.json
        character_name = data.get("name", "").strip()
        
        # Validate input
        if not character_name:
            return jsonify({"error": "Please enter a name"}), 400
        
        if len(character_name) > 50:
            return jsonify({"error": "Name is too long (max 50 characters)"}), 400
        
        # Read story and replace placeholder
        story = read_story()
        story_with_name = story.replace("[NAME]", character_name)
        
        # Generate audio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        output_file = loop.run_until_complete(generate_audio(story_with_name, character_name))
        
        return jsonify({
            "success": True,
            "filename": output_file.name,
            "message": f"Audio generated successfully for {character_name}!",
            "playlist": list_audio_files()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    """Download the generated audio file"""
    try:
        # Security: only allow files from output directory
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists() or not file_path.is_file():
            return jsonify({"error": "File not found"}), 404
        
        return send_file(
            str(file_path),
            as_attachment=True,
            mimetype="audio/mpeg"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Additional utility endpoints
@app.route("/list_audio", methods=["GET"])
def get_list():
    """Return list of available audio files"""
    return jsonify({"files": list_audio_files()}), 200

@app.route("/generate_playlist", methods=["POST"])
def generate_playlist():
    """Generate a sequence of audio files by splitting story into sections."""
    try:
        data = request.json
        character_name = data.get("name", "").strip()
        if not character_name:
            return jsonify({"error": "Please enter a name"}), 400
        
        if len(character_name) > 50:
            return jsonify({"error": "Name is too long (max 50 characters)"}), 400
        
        # read & split story
        story = read_story()
        sections = split_story(story)
        generated = []
        # ensure we have an event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        for idx, section in enumerate(sections, start=1):
            text = section.replace("[NAME]", character_name)
            output_file = loop.run_until_complete(generate_audio(text, character_name))
            generated.append(output_file.name)
        
        return jsonify({
            "success": True,
            "files": generated,
            "playlist": list_audio_files(),
            "message": f"Generated {len(generated)} sections for {character_name}."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
