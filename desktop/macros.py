"""
PC Automation Macros — launch preset app groups by voice.
User can define their own setups.
"""
import subprocess
import os
import time
import webbrowser
from memory import _load, _save

def get_memory(key):
    return _load().get(key)

def setMemory(key, value):
    mem = _load()
    mem[key] = value
    _save(mem)

DEFAULT_MACROS = {
    "work setup": [
        {"type": "app", "cmd": "code"},           # VS Code
        {"type": "url", "url": "https://gmail.com"},
        {"type": "url", "url": "https://github.com"},
    ],
    "study setup": [
        {"type": "app", "cmd": "notepad"},
        {"type": "url", "url": "https://youtube.com"},
        {"type": "url", "url": "https://notion.so"},
    ],
    "entertainment": [
        {"type": "uri", "uri": "spotify:"},
        {"type": "url", "url": "https://youtube.com"},
        {"type": "url", "url": "https://netflix.com"},
    ],
    "morning routine": [
        {"type": "url", "url": "https://gmail.com"},
        {"type": "url", "url": "https://news.google.com"},
        {"type": "uri", "uri": "spotify:"},
    ]
}

def run_macro(name):
    name = name.lower().strip()
    macros = DEFAULT_MACROS
    # Also check user-saved macros from memory
    saved = get_memory("macros") or {}
    macros.update(saved)

    if name not in macros:
        available = ", ".join(macros.keys())
        return f"No macro named '{name}'. Available: {available}"

    steps = macros[name]
    for step in steps:
        try:
            if step["type"] == "app":
                subprocess.Popen(step["cmd"], shell=True)
            elif step["type"] == "url":
                webbrowser.open(step["url"])
            elif step["type"] == "uri":
                os.startfile(step["uri"])
            time.sleep(0.5)
        except Exception:
            pass
    return f"{name.title()} launched."

def list_macros():
    names = list(DEFAULT_MACROS.keys())
    saved = get_memory("macros") or {}
    names += list(saved.keys())
    return "Available setups: " + ", ".join(names)

def save_macro(name, steps):
    saved = get_memory("macros") or {}
    saved[name] = steps
    setMemory("macros", saved)
    return f"Macro '{name}' saved."
