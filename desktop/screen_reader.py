import subprocess
import pyperclip

def get_active_window_title():
    result = subprocess.run(
        ['powershell', '-Command',
         '(Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Sort-Object CPU -Descending | Select-Object -First 1).MainWindowTitle'],
        capture_output=True, text=True
    )
    return result.stdout.strip() or "Unknown window"

def read_screen_text():
    """Return active window title — safe, no keyboard shortcuts."""
    title = get_active_window_title()
    return f"Active window: {title}"

def get_clipboard_summary():
    text = pyperclip.paste()
    if not text:
        return "Clipboard is empty."
    if len(text) < 200:
        return text
    return text[:200] + "..."
