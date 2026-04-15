"""
Terminal test mode — type commands instead of speaking.
Tests the full brain pipeline without needing mic or wake word.
Run: python test_terminal.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check .env exists
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if not os.path.exists(env_path):
    print("\n[!] No .env file found.")
    print(f"    Copy .env.example to .env and add your GROQ_API_KEY")
    print(f"    Path: {os.path.abspath(env_path)}\n")
    sys.exit(1)

from brain import process_command
import memory

def run():
    name = memory.get_preference("user_name")
    if name:
        print(f"\n[Pragya] Welcome back, {name}. Type your commands below.")
    else:
        print("\n[Pragya] Hi! What's your name?")
        name = input("You: ").strip().capitalize()
        if name:
            memory.set_preference("user_name", name)
            print(f"[Pragya] Nice to meet you, {name}.\n")

    print("[Pragya] Ready. Type a command or question. Type 'quit' to exit.\n")
    print("  Examples:")
    print("  - what time is it")
    print("  - open notepad")
    print("  - how are you")
    print("  - what's my battery")
    print("  - search for python tutorials")
    print("  - volume up")
    print("  - take a screenshot\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[Pragya] Shutting down. Bye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'bye'):
            print("[Pragya] Later.")
            break

        try:
            reply = process_command(user_input)
            print(f"[Pragya] {reply}\n")
        except Exception as e:
            print(f"[Error] {e}\n")

if __name__ == "__main__":
    run()
