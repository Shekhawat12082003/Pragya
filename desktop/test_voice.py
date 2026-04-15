"""
Voice test mode — speak a command, hear the reply.
No wake word needed. Just runs listen → think → speak in a loop.
Run: python test_voice.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice import speak, listen_once
from brain import process_command

def main():
    speak("Voice test mode. I'm listening. Speak your command.")
    print("\n[Voice Test] Speak after the prompt. Say 'stop' to exit.\n")

    while True:
        print("[Listening...]")
        command = listen_once(timeout=10, phrase_limit=20)

        if not command:
            speak("Didn't catch that. Try again.")
            continue

        print(f"[You] {command}")

        if command.strip() in ("stop", "exit", "quit", "bye"):
            speak("Stopping voice test. Bye.")
            break

        result = process_command(command)
        if result:
            speak(result)

if __name__ == "__main__":
    main()
