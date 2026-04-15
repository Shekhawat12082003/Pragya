"""
MODULE 2: TASK EXECUTION
All system-level actions Pragya can perform on Windows.
"""

import os
import subprocess
import webbrowser
import urllib.parse
import time
import threading
import pyautogui
from datetime import datetime

import pyperclip

def _wa_type(text):
    """Type text via clipboard to handle spaces and special chars."""
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

APP_MAP = {
    'whatsapp':      'whatsapp:',
    'spotify':       'spotify:',
    'notepad':       'notepad.exe',
    'calculator':    'calc.exe',
    'chrome':        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'file explorer': 'explorer.exe',
    'settings':      'ms-settings:',
    'camera':        'microsoft.windows.camera:',
    'photos':        'ms-photos:',
}

def open_app(app_name):
    name = app_name.lower().strip()
    if name == 'youtube':
        webbrowser.open('https://youtube.com')
        return "Opening YouTube."
    if name == 'gmail':
        webbrowser.open('https://mail.google.com')
        return "Opening Gmail."
    for key, cmd in APP_MAP.items():
        if key in name:
            if cmd.endswith(':'):
                os.startfile(cmd)
            else:
                subprocess.Popen(cmd)
            return f"Opening {key}."
    subprocess.Popen(['start', '', app_name], shell=True)
    return f"Trying to open {app_name}."

# ── WhatsApp Desktop App ──────────────────────────────────────────────────────

def whatsapp_open_chat(contact):
    import subprocess
    subprocess.Popen(['cmd', '/c', 'start', 'whatsapp:'])
    time.sleep(4)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.8)
    pyautogui.hotkey('ctrl', 'a')
    _wa_type(contact)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(1)
    return f"Opened chat with {contact}."

def whatsapp_send_message(contact, message):
    import subprocess
    subprocess.Popen(['cmd', '/c', 'start', 'whatsapp:'])
    time.sleep(4)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.8)
    pyautogui.hotkey('ctrl', 'a')
    _wa_type(contact)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(1.5)
    _wa_type(message)
    time.sleep(0.5)
    pyautogui.press('enter')
    return f"Message sent to {contact}."

# ── Calls ─────────────────────────────────────────────────────────────────────

def make_call(contact):
    webbrowser.open(f"tel:{contact}")
    return f"Initiating call to {contact}."

# ── Web ───────────────────────────────────────────────────────────────────────

def open_url(url):
    if not url.startswith('http'):
        url = 'https://' + url
    webbrowser.open(url)
    return f"Opened {url}."

def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
    return f"Searching for: {query}."

def play_youtube(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
    return f"Searching YouTube for {query}."

def play_spotify(query):
    try:
        os.startfile(f"spotify:search:{urllib.parse.quote(query)}")
        return f"Playing {query} on Spotify."
    except Exception:
        webbrowser.open(f"https://open.spotify.com/search/{urllib.parse.quote(query)}")
        return f"Opened Spotify search for {query}."

# ── System ────────────────────────────────────────────────────────────────────

def take_screenshot():
    path = os.path.join(os.path.expanduser("~"), "Desktop", f"pragya_{int(time.time())}.png")
    pyautogui.screenshot(path)
    return f"Screenshot saved to Desktop."

def get_time():
    now = datetime.now()
    return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}."

def set_reminder(text, minutes=5):
    def _remind():
        time.sleep(minutes * 60)
        try:
            from plyer import notification
            notification.notify(title="Pragya Reminder", message=text, timeout=10)
        except Exception:
            pass
        from voice import speak
        speak(f"Reminder: {text}")
    threading.Thread(target=_remind, daemon=True).start()
    return f"Reminder set for {minutes} minute{'s' if minutes != 1 else ''}."
