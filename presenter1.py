import sounddevice as sd
import queue
import threading
import numpy as np
from faster_whisper import WhisperModel

samplerate = 16000
block_duration = 0.5
chunk_duration = 3
channels = 1


frames_per_block = int(samplerate * block_duration)
frames_per_chunk = int(samplerate * chunk_duration)

audio_queue = queue.Queue()
audio_buffer = []

model = WhisperModel("small", compute_type="int8")

def audio_callback(in_data, frames, time, status):
    if status:
        print(status)
    audio_queue.put(in_data.copy())

def recorder():
    with sd.InputStream(samplerate=samplerate , channels=channels ,
                        callback=audio_callback , blocksize=frames_per_block):
        print("listening ...")
        while True:
            sd.sleep(100)

def transcriber():
    global audio_buffer
    while True:
        block = audio_queue.get()
        audio_buffer.append(block)

        total_frames = sum(len(b) for b in audio_buffer)
        if total_frames >= frames_per_chunk:

            # audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
            # audio_buffer = audio_buffer[frames_per_chunk:]
            audio_data_full = np.concatenate(audio_buffer)
            audio_data = audio_data_full[:frames_per_chunk]
            leftover = audio_data_full[frames_per_chunk:]
            audio_buffer = [leftover] if len(leftover) > 0 else []

            audio_data = audio_data.flatten().astype(np.float32)

            volume = np.abs(audio_data).mean()
            if volume < 0.01:
                continue

            segments , _ = model.transcribe(
                audio_data,
                language="en",
                beam_size=1  ,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms = 500)
            )
            has_text = False
            for segment in segments:
                print(f'{segment.text}')


threading.Thread(target = recorder , daemon = True).start()
transcriber()