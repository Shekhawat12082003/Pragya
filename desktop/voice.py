import os
import speech_recognition as sr
import sounddevice as sd

# Absolute paths for model files — works regardless of cwd
_DIR = os.path.dirname(os.path.abspath(__file__))
_ONNX = os.path.join(_DIR, "kokoro-v1.0.onnx")
_VOICES = os.path.join(_DIR, "voices-v1.0.bin")

VOICE = "af_heart"   # af_heart, af_bella, bf_emma, bm_george, am_adam
_kokoro = None

def _get_kokoro():
    global _kokoro
    if _kokoro is None:
        print("[TTS] Loading Kokoro...")
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(_ONNX, _VOICES)
        print("[TTS] Kokoro ready.")
    return _kokoro

def speak(text):
    if not text:
        return
    # Cap long responses — don't read walls of text
    if len(text) > 220:
        first = text.split('.')[0].strip()
        text = first if len(first) > 10 else text[:180] + "..."
    print(f"\n[Pragya] {text}\n")
    try:
        kokoro = _get_kokoro()
        samples, rate = kokoro.create(text, voice=VOICE, speed=1.1, lang="en-us")
        sd.play(samples, rate)
        sd.wait()
    except Exception as e:
        print(f"[TTS] Kokoro error: {e} — using Edge TTS fallback")
        _speak_edge(text)

def _speak_edge(text):
    import asyncio
    import edge_tts
    import pygame
    import tempfile
    pygame.mixer.init()
    async def _run():
        communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp = f.name
        await communicate.save(tmp)
        pygame.mixer.music.load(tmp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.unlink(tmp)
    try:
        asyncio.run(_run())
    except Exception as e:
        print(f"[TTS] Edge TTS also failed: {e}")

def listen_once(timeout=6, phrase_limit=12):
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            text = r.recognize_google(audio)
            print(f"[You] {text}")
            return text.lower().strip()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except Exception as e:
            print(f"[Voice Error] {e}")
            return None
