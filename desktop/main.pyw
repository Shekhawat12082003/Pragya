import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice import speak, listen_once
from wake_word import wait_for_wake_word
from brain import process_command
import memory

STOP_WORDS    = {"stop", "sleep", "goodbye", "bye", "that's all", "go to sleep"}
CONFIRM_WORDS = {"send", "call", "delete", "email"}

def get_greeting():
    hour = datetime.now().hour
    if hour < 12:   time_greet = "Good morning"
    elif hour < 17: time_greet = "Good afternoon"
    elif hour < 21: time_greet = "Good evening"
    else:           time_greet = "Hey"
    name = memory.get_preference("user_name")
    if name:
        return f"{time_greet}, {name}. Pragya online and ready."
    else:
        return f"{time_greet}. Pragya online. What's your name?"

def ask_name_if_unknown():
    name = memory.get_preference("user_name")
    if not name:
        speak("I don't think we've met. What should I call you?")
        response = listen_once(timeout=8)
        if response:
            for filler in ["my name is", "i am", "i'm", "call me", "it's", "its"]:
                response = response.replace(filler, "").strip()
            name = response.strip().capitalize()
            memory.set_preference("user_name", name)
            speak(f"Got it. Nice to meet you, {name}.")

def conversation_loop():
    speak("Yes?")
    while True:
        command = listen_once(timeout=8, phrase_limit=20)
        if not command:
            speak("Still here.")
            command = listen_once(timeout=5, phrase_limit=20)
            if not command:
                speak("Going back to sleep. Say Pragya when you need me.")
                return
        if any(w in command for w in STOP_WORDS):
            speak("Alright, going to sleep.")
            return
        needs_confirm = any(w in command for w in CONFIRM_WORDS)
        if needs_confirm:
            speak("Should I go ahead?")
            confirm = listen_once(timeout=5)
            if not confirm or not any(w in confirm for w in ["yes", "yeah", "do it", "confirm", "sure", "go ahead"]):
                speak("Cancelled.")
                continue
        result = process_command(command)
        if result:
            speak(result)

def on_wake():
    conversation_loop()

def main():
    speak(get_greeting())
    ask_name_if_unknown()
    wait_for_wake_word(on_wake)

if __name__ == "__main__":
    main()
