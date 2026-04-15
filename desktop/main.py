"""
main.py — Pragya entry point.
Say "Pragya" to activate, keep talking, say "stop/bye/sleep" to dismiss.
Auto-starts with Windows via install_startup.py
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice import speak, listen_once
from wake_word import wait_for_wake_word
from brain import process_command
import memory

# ── Optional modules — fail silently ──────────────────────────
try:
    from tray import start_tray, set_status
    _tray = True
except Exception:
    _tray = False
    def set_status(s): pass

try:
    from ws_server import start_ws_server, broadcast
    _ws = True
except Exception:
    _ws = False
    def broadcast(d): pass

# ── Constants ──────────────────────────────────────────────────
STOP_WORDS    = {"stop", "sleep", "goodbye", "bye", "that's all", "go to sleep", "band ho", "so ja"}
CONFIRM_WORDS = {"send", "call", "delete", "email"}

# ── Greeting ───────────────────────────────────────────────────
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:   greet = "Good morning"
    elif hour < 17: greet = "Good afternoon"
    elif hour < 21: greet = "Good evening"
    else:           greet = "Hey"
    name = memory.get_preference("user_name")
    return f"{greet}, {name}. Pragya online." if name else f"{greet}. Pragya online. What's your name?"

def ask_name_if_unknown():
    if memory.get_preference("user_name"):
        return
    speak("I don't think we've met. What should I call you?")
    response = listen_once(timeout=8)
    if response:
        for filler in ["my name is", "i am", "i'm", "call me", "it's", "its"]:
            response = response.replace(filler, "").strip()
        name = response.strip().capitalize()
        memory.set_preference("user_name", name)
        speak(f"Got it. Nice to meet you, {name}.")

# ── Conversation loop ──────────────────────────────────────────
def conversation_loop():
    set_status("listening")
    broadcast({"type": "state", "state": "listening"})
    speak("Yes?")
    silence_count = 0

    while True:
        command = listen_once(timeout=10, phrase_limit=20)

        if not command:
            silence_count += 1
            if silence_count >= 3:   # 30s silence → sleep
                set_status("sleeping")
                broadcast({"type": "state", "state": "idle"})
                return
            continue

        silence_count = 0
        print(f"[You] {command}")
        broadcast({"type": "command", "text": command})

        # Stop words
        if any(w in command for w in STOP_WORDS):
            speak("Okay.")
            set_status("sleeping")
            broadcast({"type": "state", "state": "idle"})
            return

        # Confirm destructive actions (word boundary check)
        if any(f" {w} " in f" {command} " for w in CONFIRM_WORDS):
            speak("Should I go ahead?")
            confirm = listen_once(timeout=5)
            if not confirm or not any(w in confirm for w in
                    ["yes", "yeah", "do it", "confirm", "sure", "go ahead", "haan", "kar do"]):
                speak("Cancelled.")
                continue

        # Process
        set_status("thinking")
        broadcast({"type": "state", "state": "thinking"})
        try:
            result = process_command(command)
        except Exception as e:
            print(f"[Error] {e}")
            result = "Something went wrong, try again."

        set_status("speaking")
        broadcast({"type": "state", "state": "speaking"})
        if result:
            speak(result)
            broadcast({"type": "response", "text": result})

        set_status("listening")
        broadcast({"type": "state", "state": "listening"})

def on_wake():
    conversation_loop()

# ── Main ───────────────────────────────────────────────────────
def main():
    print("=" * 45)
    print("  PRAGYA — Starting up")
    print("=" * 45)

    if _tray:
        start_tray()
    if _ws:
        start_ws_server()

    speak(get_greeting())
    ask_name_if_unknown()
    wait_for_wake_word(on_wake)

if __name__ == "__main__":
    main()
