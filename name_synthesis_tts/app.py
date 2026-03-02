from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import asyncio
import edge_tts
from datetime import datetime

app = Flask(__name__)

# configuration - same story file
STORY_PATH = Path("/workspaces/TTS/input/hindi_story_v2.txt")
OUTPUT_DIR = Path("/workspaces/TTS/output/name_synthesis")
BASE_DIR = OUTPUT_DIR / "base"
CUSTOM_DIR = OUTPUT_DIR / "custom"
for d in (OUTPUT_DIR, BASE_DIR, CUSTOM_DIR):
    d.mkdir(exist_ok=True, parents=True)

VOICE = "hi-IN-MadhurNeural"
SECTION_DELIMITER = "\n\n"

async def tts_generate(text: str, suffix: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{suffix}_{timestamp}.mp3"
    out = OUTPUT_DIR / fname
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(out))
    return out


def read_story() -> str:
    return STORY_PATH.read_text(encoding="utf-8")


def split_story(text: str) -> list[str]:
    return [p.strip() for p in text.split(SECTION_DELIMITER) if p.strip()]


def prepare_base():
    parts = split_story(read_story())
    running = asyncio.get_event_loop()
    saved = []
    for idx, part in enumerate(parts):
        out = running.run_until_complete(tts_generate(part, f"base_{idx}"))
        dest = BASE_DIR / out.name
        out.rename(dest)
        saved.append(dest.name)
    return saved


def concat(name: str) -> Path:
    # create name clip
    running = asyncio.get_event_loop()
    name_audio = running.run_until_complete(tts_generate(name, "name"))
    from pydub import AudioSegment
    combined = AudioSegment.empty()
    base_files = sorted(p.name for p in BASE_DIR.glob("*.mp3"))
    for i, fname in enumerate(base_files):
        combined += AudioSegment.from_file(BASE_DIR / fname)
        if i < len(base_files)-1:
            combined += AudioSegment.from_file(name_audio)
    outname = CUSTOM_DIR / f"story_{name}.mp3"
    combined.export(outname, format="mp3")
    return outname

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prepare", methods=["POST"])
def do_prepare():
    files = prepare_base()
    return jsonify({"saved": files})

@app.route("/synthesize", methods=["POST"])
def do_synth():
    data = request.json
    name = data.get("name","" ).strip()
    if not name:
        return jsonify({"error":"Enter name"}),400
    out = concat(name)
    return jsonify({"file": out.name})

@app.route("/download/<filename>")
def download(filename):
    f = CUSTOM_DIR / filename
    if not f.exists():
        return jsonify({"error":"not found"}),404
    return send_file(str(f), as_attachment=True)

if __name__=="__main__":
    app.run(port=5002, debug=True)
