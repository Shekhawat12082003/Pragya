import speech_recognition as sr

WAKE_WORDS = {"pragya", "praga", "priya", "progya", "pragiya", "prajya"}

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
