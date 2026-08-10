# 🎙️ Real-Time Speech-to-Text with Word Export

A Python tool that turns your speech into text in real time using the **Whisper** model, and automatically saves the text into a Word (`.docx`) file.

## ✨ Features

- 🎤 Continuous, low-latency microphone recording
- 🧠 Transcription powered by [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) — a fast, optimized version of Whisper that runs well on CPU
- 📝 Automatically writes the transcribed text into a Word file
- 🔇 Smart silence filtering (VAD) to avoid wrong transcriptions during silence
- ⌨️ Stop the program anytime with a hotkey (ESC)
- 🧵 Multi-threaded design so recording and transcription happen at the same time, without blocking each other

## 🏗️ How It Works

```
Microphone → continuous recording in small blocks → Queue
           → blocks are collected until they reach a 2-second chunk
           → chunk is transcribed with faster-whisper (+ VAD filter)
           → text is written into transcript.docx
```

## 📦 Requirements

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/) installed and added to your system PATH

## 🚀 Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python faster_whisper.py
```

Once running, you'll see `listening ...` in the terminal — start speaking. The text appears live in the terminal and is also saved to `transcript.docx`. Press **ESC** to stop the program.

## ⚙️ Settings You Can Change

At the top of the main file, you can adjust these values:

| Variable | What it does | Default |
|---|---|---|
| `chunk_duration` | Length of each audio chunk before transcription (seconds) | `2` |
| `language` | Spoken language (ISO code, e.g. `"en"` or `"fa"`) | `"en"` |


## 🛠️ Built With

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [sounddevice](https://python-sounddevice.readthedocs.io/)
- [python-docx](https://python-docx.readthedocs.io/)

## 📌 Known Limitations

- Currently only supports live microphone input (not pre-recorded audio files)
- Transcription accuracy depends on microphone quality and background noise


