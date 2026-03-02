# TTS

This repository contains a small notebook and example code to generate speech audio from text using two different libraries:

- `gTTS` — Google Text-to-Speech (simple, offline save via API wrapper)
- `edge-tts` — Microsoft Edge / Azure neural voices (async, higher quality voices available)

The notebook reads a Hindi story from `input/hindi_story.txt` and saves spoken audio (MP3) to the workspace.

Getting started
---------------

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Upgrade `pip` and install dependencies from `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the notebook in Jupyter or open `tts-test.ipynb` in VS Code and run the cells.

Notes on usage
--------------

- In a script (non-interactive) the notebook code will call `asyncio.run()` to execute the `edge-tts` coroutine and save `story_audio.mp3`.
- In interactive environments (Jupyter / VS Code notebooks) an event loop may already be running. Use `await generate_audio()` in a notebook cell or the provided `run_coro()` helper which schedules the coroutine safely.
- The Hindi story used for synthesis is read from `input/hindi_story.txt` so you can swap that file to change the spoken content.

Troubleshooting
---------------

- If you see `RuntimeError: asyncio.run() cannot be called from a running event loop`, run `await generate_audio()` in a notebook cell or use `run_coro(generate_audio())` (the notebook contains a helper). 
- If `edge-tts` fails due to network or authentication issues, ensure internet access and consult the `edge-tts` docs for additional configuration.

Files of interest
---------------

- `tts-test.ipynb` — main notebook with examples for `gTTS` and `edge-tts`.
- `input/hindi_story.txt` — example Hindi story read by the notebook.
- `requirements.txt` — Python dependencies for easy setup.

License / Notes
----------------
This is a small example project for local experimentation with TTS libraries. Be mindful of license and API usage limits for third-party services.
