# 🎙️ Voice-Controlled PowerPoint Presenter

A Python assistant that lets you control a live PowerPoint slideshow with your voice. Say a wake word, then speak a command — the app transcribes it with **FasterWhisper** and executes it directly on PowerPoint through the Windows COM API.

## ✨ Features

- 🎤 Continuous, low-latency microphone listening with a two-stage pipeline (lightweight wake-word detection + accurate command transcription)
- 🧠 Powered by [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) — fast, CPU-friendly Whisper inference
- 🔑 Wake word ("Assistant") to activate, spoken "sleep" to deactivate — no need to repeat the wake word for every command
- 🎯 Fuzzy command matching with [`rapidfuzz`](https://github.com/rapidfuzz/RapidFuzz) — tolerant of Whisper's occasional mis-transcriptions
- 🖥️ Direct PowerPoint control via `win32com.client` (COM API) — works regardless of which window has focus, and can jump to any slide number
- 🔇 Silence and low-volume filtering to avoid false transcriptions
- 🧵 Multi-threaded design — recording never blocks while a command is being processed

## 🏗️ How It Works

```
Microphone → continuous recording in small blocks → Queue
           → WAITING_FOR_WAKE: short chunks transcribed with a lightweight model
                → wake word detected (fuzzy match) → LISTENING_COMMAND
           → LISTENING_COMMAND: longer chunks transcribed with a more accurate model
                → command matched (fuzzy match) → executed on PowerPoint via COM
                → "sleep" detected → back to WAITING_FOR_WAKE
```

## 📦 Requirements

- Python 3.9+
- Windows (COM automation requires `pywin32`)
- Microsoft PowerPoint (desktop app) installed and open, with a slideshow running

## 🚀 Setup

```bash
# Clone the repository
git clone https://github.com/Myasin3201/faster_whisper-RealTime.git
cd faster_whisper-RealTime

# Create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

1. Open your presentation in PowerPoint and start the slideshow (F5).
2. Run the assistant:

```bash
python ai_presenter.py
```

3. Say **"Assistant"** to activate, then speak a command:
   - "next slide" / "next page"
   - "previous slide" / "previous page"
   - "go to slide five"
4. Say **"sleep"** to stop listening for commands until the wake word is said again.

## ⚙️ Settings You Can Change

At the top of `ai_presenter.py`:

| Variable | What it does | Default |
|---|---|---|
| `WAKE_WORD` | Word that activates command listening | `"assistant"` |
| `OFF_WORD` | Word that deactivates command listening | `"sleep"` |
| `WAKE_THRESHOLD` | Fuzzy-match confidence (0–100) required to trigger wake/sleep | `70` |
| `WAKE_CHUNK_DURATION` | Audio chunk length while waiting for the wake word (seconds) | `2.5` |
| `COMMAND_CHUNK_DURATION` | Audio chunk length while listening for a command (seconds) | `4.0` |

Command phrases and their fuzzy-match threshold can be adjusted in `ppt_controller.py` under `COMMAND_PATTERNS`.

## 🛠️ Built With

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [sounddevice](https://python-sounddevice.readthedocs.io/)
- [rapidfuzz](https://github.com/rapidfuzz/RapidFuzz)
- [pywin32](https://github.com/mhammond/pywin32) (`win32com.client`)

## 📁 Project Structure

```
ai_presenter.py     # audio pipeline: recording, wake-word detection, command transcription
ppt_controller.py   # PowerPoint control via COM API + command matching
```

## 📌 Known Limitations

- Requires PowerPoint to already be open with an active slideshow — the app connects to a running instance, it doesn't launch one
- English commands only for now
- Transcription accuracy depends on microphone quality and background/classroom noise
- No speaker identification — anyone's voice near the mic can trigger a command