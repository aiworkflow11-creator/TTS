# Name‑synthesis TTS App

This version first converts the story text (without names) into base audio segments. Later, you can supply a name and the app will insert a recording of that name between each segment, producing a full story in the cloned voice.

## Installation

```
cd /workspaces/TTS/name_synthesis_tts
pip install -r ../requirements.txt pydub
```

(`pydub` is required for concatenation; `ffmpeg` may also be needed in PATH.)

## Usage

1. Run the server:
   ```bash
   python app.py
   ```
   Opens on port **5002**.

2. Click **Prepare base audio** on the homepage. This will create files in `output/name_synthesis/base/segment_*.mp3`.

3. Enter a character name and press *Synthesize story*. The story (with name interleaved) will be generated in `output/name_synthesis/custom/` and played automatically.

4. Download the result using the link.

## Workflow

- **/prepare**: splits the story and generates TTS for each section once (no names).
- **/synthesize**: takes a name, generates a name clip if needed, concatenates all segments and returns a single MP3.

This keeps GPU usage minimal — the expensive long text is processed only once.
