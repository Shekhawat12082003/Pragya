"""
Train a custom "Pragya" wake word using OpenWakeWord.
Run this once to create your personal wake word model.

Steps:
1. Run this script
2. Say "Pragya" clearly 5 times when prompted
3. Model gets saved as pragya_wakeword.onnx
4. Pragya will use it automatically
"""

import os
import sys
import wave
import pyaudio
import numpy as np

RECORDINGS_DIR = "wakeword_recordings"
WAKE_WORD = "pragya"
NUM_SAMPLES = 5          # how many times you record the word
SAMPLE_RATE = 16000
DURATION = 2             # seconds per recording

def record_sample(index):
    """Record a single 2-second audio sample."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=SAMPLE_RATE, input=True,
                    frames_per_buffer=1024)

    print(f"\n  [{index+1}/{NUM_SAMPLES}] Say 'Pragya' clearly in 3... 2... 1... GO!")
    import time; time.sleep(1.5)
    print("  🎙 Recording...")

    frames = []
    for _ in range(0, int(SAMPLE_RATE / 1024 * DURATION)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("  ✓ Done.")

    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    path = os.path.join(RECORDINGS_DIR, f"{WAKE_WORD}_{index}.wav")
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))
    return path

def train():
    print("=" * 50)
    print("  PRAGYA Wake Word Trainer")
    print("=" * 50)
    print("\nYou'll record yourself saying 'Pragya' 5 times.")
    print("Speak clearly, at normal volume, in a quiet room.")
    input("\nPress Enter when ready...")

    paths = []
    for i in range(NUM_SAMPLES):
        path = record_sample(i)
        paths.append(path)

    print("\n[Training] Building wake word model...")
    try:
        from openwakeword.custom_verifier_model import train_custom_verifier
        train_custom_verifier(
            positive_reference_clips=paths,
            output_path="pragya_wakeword.onnx",
            model_name=WAKE_WORD
        )
        print("\n✓ Wake word model saved as: pragya_wakeword.onnx")
        print("✓ Pragya will now wake up when you say 'Pragya'!")
        update_wake_word_file()
    except Exception as e:
        print(f"\n[!] Training failed: {e}")
        print("Falling back to STT-based wake detection instead.")
        use_stt_fallback()

def update_wake_word_file():
    """Update wake_word.py to use the custom model."""
    content = open("wake_word.py").read()
    # Switch to custom model
    new_content = content.replace(
        'WAKE_WORD = "hey_jarvis"',
        'WAKE_WORD = "pragya"'
    ).replace(
        'oww = Model(wakeword_models=[WAKE_WORD], inference_framework="onnx")',
        'oww = Model(wakeword_models=["pragya_wakeword.onnx"], inference_framework="onnx")'
    )
    open("wake_word.py", "w").write(new_content)
    print("✓ wake_word.py updated to use custom 'Pragya' model.")

def use_stt_fallback():
    """If training fails, switch to STT-based wake detection."""
    fallback = '''"""
Wake word detection — STT fallback (no model needed).
Listens for the word "pragya" via Google Speech Recognition.
"""

import speech_recognition as sr

WAKE_WORDS = {"pragya", "praga", "priya", "progya", "pragiya"}

def wait_for_wake_word(callback):
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.6

    print("[Pragya] Listening for wake word... say 'Pragya'")

    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source, timeout=None, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio).lower().strip()
                words = set(text.split())
                if words & WAKE_WORDS:
                    print(f"[Wake] Triggered: '{text}'")
                    callback()
                    print("[Pragya] Listening for wake word... say 'Pragya'")
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                continue
        except Exception:
            continue
'''
    open("wake_word.py", "w").write(fallback)
    print("✓ Switched to STT wake detection. Say 'Pragya' to activate.")

if __name__ == "__main__":
    train()
