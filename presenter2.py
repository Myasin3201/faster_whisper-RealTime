import sounddevice as sd
import queue
import threading
import numpy as np
from faster_whisper import WhisperModel
from rapidfuzz import fuzz

samplerate = 16000
channels = 1

WAKE_BLOCK_DURATION = 0.5
WAKE_CHUNK_DURATION = 2.5 # 1.5
COMMAND_CHUNK_DURATION = 4.0 # 3

WAKE_WORD = "assistant"
WAKE_THRESHOLD = 70

frames_per_block = int(samplerate * WAKE_BLOCK_DURATION)

audio_queue = queue.Queue()
audio_buffer = []

wake_model = WhisperModel("tiny", compute_type="int8")
command_model = WhisperModel("small", compute_type="int8")

state = "WAITING_FOR_WAKE"


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

def get_chunk(duration_sec , overlap_sec = 0.5):

    global audio_buffer
    needed_frames = int(samplerate * duration_sec)
    overlap_frames = int(samplerate * overlap_sec)

    while True:
        block = audio_queue.get()
        audio_buffer.append(block)
        total = sum(len(b) for b in audio_buffer)
        if total >= needed_frames:
            full = np.concatenate(audio_buffer).flatten().astype(np.float32)
            chunk = full[:needed_frames]
            keep_from = needed_frames - overlap_frames
            leftover = full[needed_frames:]
            audio_buffer = [leftover] if len(leftover) > 0 else []
            return chunk
WAKE_PROMPT = "Assistant"
COMMAND_PROMPT =  "next slide, previous slide, go to slide , next page , previous page , go to page "
def transcribe(model, audio_data , prompt = WAKE_PROMPT):
    volume = np.abs(audio_data).mean()
    if volume < 0.01:
        return ""
    segments, _ = model.transcribe(
        audio_data, language="en", beam_size=1,
        vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300) ,
        initial_prompt=prompt
        # condition_on_previous_text=False,
        # temperature=0.0,no_speech_threshold=0.6
    )
    return " ".join(seg.text for seg in segments).strip()

def wake_word_detected(text):
    if not text:
        return False
    score = fuzz.partial_ratio(WAKE_WORD.lower(), text.lower())
    return score >= WAKE_THRESHOLD


def main_loop():
    global state
    while True:
        if state == "WAITING_FOR_WAKE":
            chunk = get_chunk(WAKE_CHUNK_DURATION)
            text = transcribe(wake_model, chunk , prompt = WAKE_PROMPT)
            if text:
                print(f" WAITING_FOR_WAKE : {text}")
            if wake_word_detected(text):
                print(" ... LISTENING_COMMAND ...")
                state = "LISTENING_COMMAND"

        elif state == "LISTENING_COMMAND":
            chunk = get_chunk(COMMAND_CHUNK_DURATION)
            command_text = transcribe(command_model, chunk , prompt = COMMAND_PROMPT)
            print(f" LISTENING_COMMAND : {command_text}")
            state = "WAITING_FOR_WAKE"

if __name__ == "__main__":
    threading.Thread(target=recorder, daemon=True).start()
    main_loop()

