"""
System tray icon — shows Pragya status in Windows taskbar.
Requires: pip install pystray pillow
"""
import threading
import pystray
from PIL import Image, ImageDraw

_tray_icon = None
_status = "sleeping"

def _create_image(color):
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=color)
    return img

STATUS_COLORS = {
    "sleeping":   (80, 80, 80),
    "listening":  (124, 106, 247),
    "thinking":   (245, 158, 11),
    "speaking":   (34, 197, 94),
}

def set_status(status):
    global _status
    _status = status
    if _tray_icon:
        color = STATUS_COLORS.get(status, (80, 80, 80))
        _tray_icon.icon = _create_image(color)
        _tray_icon.title = f"Pragya — {status.capitalize()}"

def start_tray():
    global _tray_icon
    menu = pystray.Menu(
        pystray.MenuItem("Pragya", lambda: None, enabled=False),
        pystray.MenuItem("Exit", lambda: _tray_icon.stop())
    )
    _tray_icon = pystray.Icon(
        "Pragya",
        _create_image(STATUS_COLORS["sleeping"]),
        "Pragya — Sleeping",
        menu
    )
    t = threading.Thread(target=_tray_icon.run, daemon=True)
    t.start()
