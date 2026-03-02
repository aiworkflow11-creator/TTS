from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path
import asyncio
import edge_tts
from datetime import datetime

app = Flask(__name__)

# Configuration for the original (single‑file) app
STORY_PATH = Path("/workspaces/TTS/input/hindi_story_v2.txt")
OUTPUT_DIR = Path("/workspaces/TTS/output/original")
OUTPUT_DIR.mkdir(exist_ok=True)
VOICE = "hi-IN-MadhurNeural"  # male Hindi voice

async def generate_audio(text: str, character_name: str) -> Path:
    """Produce a single MP3 file for supplied text."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_name = "".join(c if c.isalnum() else "_" for c in character_name)
    output_file = OUTPUT_DIR / f"story_{safe_name}_{timestamp}.mp3"
    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate="-8%",
        pitch="+0Hz",
        volume="-5%"
    )
    await communicate.save(str(output_file))
    return output_file

@app.route("/")
def index():
    return render_template("index_original.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Please enter a name"}), 400
    story = STORY_PATH.read_text(encoding="utf-8").replace("[NAME]", name)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    out = loop.run_until_complete(generate_audio(story, name))
    return jsonify({
        "success": True,
        "filename": out.name,
        "message": f"Audio ready for {name}!"
    })

@app.route("/download/<filename>")
def download(filename):
    f = OUTPUT_DIR / filename
    if not f.exists():
        return jsonify({"error": "Not found"}), 404
    return send_file(str(f), as_attachment=True, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
