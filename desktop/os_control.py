"""
OS CONTROL MODULE
Full Windows automation — mouse, keyboard, files, processes, system settings.
"""

import os
import subprocess
import psutil
import pyautogui
import time
import threading
import glob
from datetime import datetime

pyautogui.FAILSAFE = True   # move mouse to top-left corner to abort

# ── Mouse & Keyboard ──────────────────────────────────────────────────────────

def click(x, y):
    pyautogui.click(x, y)
    return f"Clicked at ({x}, {y})."

def type_text(text):
    pyautogui.typewrite(text, interval=0.04)
    return f"Typed: {text}"

def press_key(key):
    """e.g. 'enter', 'escape', 'ctrl+c', 'alt+tab', 'win'"""
    keys = key.lower().split('+')
    if len(keys) > 1:
        pyautogui.hotkey(*keys)
    else:
        pyautogui.press(keys[0])
    return f"Pressed {key}."

def scroll(direction="down", amount=3):
    amt = -amount if direction == "down" else amount
    pyautogui.scroll(amt)
    return f"Scrolled {direction}."

def get_mouse_position():
    x, y = pyautogui.position()
    return f"Mouse is at ({x}, {y})."

# ── Window Management ─────────────────────────────────────────────────────────

def switch_window():
    pyautogui.hotkey('alt', 'tab')
    return "Switched window."

def minimize_window():
    pyautogui.hotkey('win', 'down')
    return "Window minimized."

def maximize_window():
    pyautogui.hotkey('win', 'up')
    return "Window maximized."

def close_window():
    pyautogui.hotkey('alt', 'f4')
    return "Window closed."

def show_desktop():
    pyautogui.hotkey('win', 'd')
    return "Showing desktop."

def open_task_manager():
    pyautogui.hotkey('ctrl', 'shift', 'esc')
    return "Task manager opened."

def lock_screen():
    pyautogui.hotkey('win', 'l')
    return "Screen locked."

def virtual_desktop_new():
    pyautogui.hotkey('win', 'ctrl', 'd')
    return "New virtual desktop created."

# ── File System ───────────────────────────────────────────────────────────────

def create_file(path, content=""):
    path = os.path.expanduser(path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    return f"File created: {path}"

def read_file(path):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return f"File not found: {path}"
    with open(path, 'r') as f:
        content = f.read(2000)  # limit to 2000 chars for voice
    return content

def delete_file(path):
    path = os.path.expanduser(path)
    if os.path.exists(path):
        os.remove(path)
        return f"Deleted: {path}"
    return f"File not found: {path}"

def list_folder(path="~/Desktop"):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return f"Folder not found: {path}"
    items = os.listdir(path)
    if not items:
        return "Folder is empty."
    return f"{len(items)} items: " + ", ".join(items[:10])

def open_file(path):
    path = os.path.expanduser(path)
    os.startfile(path)
    return f"Opened {path}."

def open_folder(path="~/Desktop"):
    path = os.path.expanduser(path)
    subprocess.Popen(f'explorer "{path}"')
    return f"Opened folder: {path}"

def find_file(name, search_in="~"):
    base = os.path.expanduser(search_in)
    matches = glob.glob(os.path.join(base, "**", f"*{name}*"), recursive=True)
    if not matches:
        return f"No files matching '{name}' found."
    return f"Found {len(matches)}: " + ", ".join(matches[:5])

# ── Process Management ────────────────────────────────────────────────────────

def list_processes():
    procs = [(p.pid, p.name()) for p in psutil.process_iter(['pid', 'name'])]
    names = [p[1] for p in procs[:15]]
    return "Running: " + ", ".join(names)

def kill_process(name):
    killed = []
    for proc in psutil.process_iter(['name']):
        if name.lower() in proc.info['name'].lower():
            proc.kill()
            killed.append(proc.info['name'])
    if killed:
        return f"Killed: {', '.join(killed)}"
    return f"No process named '{name}' found."

def run_command(cmd):
    """Run any shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=15
        )
        out = (result.stdout or result.stderr or "Done.").strip()
        return out[:300]  # cap for voice
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Error: {e}"

# ── System Settings ───────────────────────────────────────────────────────────

def set_volume(level: int):
    """Set volume 0–100 using PowerShell (no extra lib needed)."""
    level = max(0, min(100, level))
    script = f"$obj = New-Object -ComObject WScript.Shell; " \
             f"1..50 | ForEach-Object {{ $obj.SendKeys([char]174) }}; " \
             f"$steps = [math]::Round({level} / 2); " \
             f"1..$steps | ForEach-Object {{ $obj.SendKeys([char]175) }}"
    # Cleaner approach via nircmd if available, else PowerShell audio API
    try:
        subprocess.run(
            ['powershell', '-Command',
             f'(New-Object -ComObject WScript.Shell).SendKeys([char]174 * 50)'],
            capture_output=True
        )
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        vol = cast(interface, POINTER(IAudioEndpointVolume))
        vol.SetMasterVolumeLevelScalar(level / 100, None)
        return f"Volume set to {level}%."
    except Exception:
        # Fallback: use keyboard volume keys
        pyautogui.hotkey('volumemute')
        return f"Could not set exact volume. Try installing pycaw: pip install pycaw comtypes"

def mute_volume():
    pyautogui.press('volumemute')
    return "Muted."

def volume_up():
    for _ in range(5): pyautogui.press('volumeup')
    return "Volume up."

def volume_down():
    for _ in range(5): pyautogui.press('volumedown')
    return "Volume down."

def get_battery():
    battery = psutil.sensors_battery()
    if not battery:
        return "No battery detected (desktop PC)."
    status = "charging" if battery.power_plugged else "on battery"
    return f"Battery at {int(battery.percent)}%, {status}."

def get_system_info():
    cpu    = psutil.cpu_percent(interval=1)
    ram    = psutil.virtual_memory()
    disk   = psutil.disk_usage('/')
    return (f"CPU: {cpu}%, "
            f"RAM: {ram.percent}% used ({round(ram.used/1e9,1)}GB of {round(ram.total/1e9,1)}GB), "
            f"Disk: {disk.percent}% used.")

def empty_recycle_bin():
    subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'], capture_output=True)
    return "Recycle bin emptied."

def shutdown(minutes=0):
    subprocess.run(f'shutdown /s /t {minutes * 60}', shell=True)
    return f"Shutting down{'in ' + str(minutes) + ' minutes' if minutes else ' now'}."

def restart(minutes=0):
    subprocess.run(f'shutdown /r /t {minutes * 60}', shell=True)
    return f"Restarting{'in ' + str(minutes) + ' minutes' if minutes else ' now'}."

def cancel_shutdown():
    subprocess.run('shutdown /a', shell=True)
    return "Shutdown cancelled."

# ── Clipboard ─────────────────────────────────────────────────────────────────

def copy_to_clipboard(text):
    subprocess.run(['powershell', '-Command', f'Set-Clipboard -Value "{text}"'])
    return f"Copied to clipboard."

def get_clipboard():
    result = subprocess.run(
        ['powershell', '-Command', 'Get-Clipboard'],
        capture_output=True, text=True
    )
    return result.stdout.strip() or "Clipboard is empty."
