"""
Adds Pragya to Windows startup so it runs automatically on login.
Run this once: python install_startup.py
"""

import os
import sys
import winreg

def install():
    # Path to this project's main.py
    desktop_dir = os.path.dirname(os.path.abspath(__file__))
    main_py     = os.path.join(desktop_dir, "main.pyw")
    python_exe  = sys.executable  # current python interpreter

    # We launch via pythonw.exe so no console window appears on startup
    pythonw = python_exe.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw):
        pythonw = python_exe  # fallback to python.exe

    command = f'"{pythonw}" "{main_py}"'

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Pragya", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        print(f"[✓] Pragya added to startup.")
        print(f"    Command: {command}")
        print(f"    Pragya will now start automatically when you log in.")
    except Exception as e:
        print(f"[✗] Failed to add to startup: {e}")

def uninstall():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "Pragya")
        winreg.CloseKey(key)
        print("[✓] Pragya removed from startup.")
    except FileNotFoundError:
        print("[!] Pragya wasn't in startup.")
    except Exception as e:
        print(f"[✗] Failed: {e}")

if __name__ == "__main__":
    if "--remove" in sys.argv:
        uninstall()
    else:
        install()
