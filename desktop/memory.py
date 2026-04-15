"""
MODULE 4: MEMORY ENGINE
Stores preferences, command history, workflows, and repetitive patterns.
"""

import json
import os
from datetime import datetime
from collections import Counter

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "pragya_memory.json")

def _load():
    if not os.path.exists(MEMORY_FILE):
        return {"preferences": {}, "history": [], "workflows": {}, "command_counts": {}}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def _save(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_command(command, action, result):
    """Log every command for pattern detection."""
    mem = _load()
    entry = {
        "time": datetime.now().isoformat(),
        "command": command,
        "action": action,
        "result": result
    }
    mem["history"].append(entry)
    mem["history"] = mem["history"][-200:]  # keep last 200

    # Track command frequency for automation detection
    key = action.get("action", "unknown") if isinstance(action, dict) else "unknown"
    mem["command_counts"][key] = mem["command_counts"].get(key, 0) + 1

    _save(mem)

def get_history(n=10):
    history = _load().get("history", [])
    # Ensure history is a list, not a string
    if isinstance(history, str):
        history = []
    return history[-n:] if history else []

def set_preference(key, value):
    mem = _load()
    mem["preferences"][key] = value
    _save(mem)

def get_preference(key, default=None):
    return _load()["preferences"].get(key, default)

def save_workflow(name, steps):
    mem = _load()
    mem["workflows"][name] = steps
    _save(mem)

def get_workflow(name):
    return _load()["workflows"].get(name)

def get_all_workflows():
    return _load()["workflows"]

def get_repetitive_actions(threshold=3):
    """Return actions done more than threshold times — candidates for automation."""
    counts = _load()["command_counts"]
    return {k: v for k, v in counts.items() if v >= threshold}

def get_context_summary():
    """Build a short memory context string to inject into GPT."""
    mem = _load()
    prefs = mem.get("preferences", {})
    history = mem.get("history", [])
    # Ensure history is a list, not a string
    if isinstance(history, str):
        history = []
    recent = history[-5:] if history else []
    workflows = list(mem.get("workflows", {}).keys())

    lines = []
    if prefs:
        lines.append(f"User preferences: {json.dumps(prefs)}")
    if recent:
        cmds = [h["command"] for h in recent]
        lines.append(f"Recent commands: {', '.join(cmds)}")
    if workflows:
        lines.append(f"Saved workflows: {', '.join(workflows)}")
    return "\n".join(lines) if lines else ""
