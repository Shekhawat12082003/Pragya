"""
Floating orb popup — shows in bottom-right corner when Pragya is active.
States: sleeping (grey), listening (purple pulse), thinking (yellow spin), speaking (green pulse)
"""
import tkinter as tk
import threading
import math
import time

class OrbWindow:
    def __init__(self):
        self.root = None
        self.state = "sleeping"
        self.angle = 0
        self.alpha = 1.0
        self.pulse_dir = -1
        self._running = False
        self.text_var = None

    def start(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)          # no title bar
        self.root.attributes('-topmost', True)    # always on top
        self.root.attributes('-transparentcolor', '#000001')
        self.root.configure(bg='#000001')

        # Position bottom-right
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 220, 80
        self.root.geometry(f"{w}x{h}+{sw-w-20}+{sh-h-60}")

        self.canvas = tk.Canvas(self.root, width=w, height=h,
                                bg='#000001', highlightthickness=0)
        self.canvas.pack()

        self.text_var = tk.StringVar(value="")
        self._running = True
        self._animate()
        self.root.mainloop()

    def _animate(self):
        if not self._running:
            return
        self.canvas.delete("all")
        self.angle = (self.angle + 3) % 360

        STATE_COLORS = {
            "sleeping":  "#444444",
            "listening": "#7c6af7",
            "thinking":  "#f59e0b",
            "speaking":  "#22c55e",
        }
        color = STATE_COLORS.get(self.state, "#444444")

        cx, cy = 40, 40
        r = 28

        # Glow rings
        if self.state != "sleeping":
            self.alpha += self.pulse_dir * 0.03
            if self.alpha <= 0.3 or self.alpha >= 1.0:
                self.pulse_dir *= -1
            for i in range(3):
                ring_r = r + (i + 1) * 8
                opacity = int(self.alpha * (3 - i) * 40)
                ring_color = self._blend(color, opacity)
                self.canvas.create_oval(
                    cx - ring_r, cy - ring_r,
                    cx + ring_r, cy + ring_r,
                    outline=ring_color, width=1
                )

        # Spinning arc for thinking
        if self.state == "thinking":
            self.canvas.create_arc(
                cx - r - 6, cy - r - 6,
                cx + r + 6, cy + r + 6,
                start=self.angle, extent=270,
                outline=color, width=2, style='arc'
            )

        # Core orb
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                fill=color, outline="")

        # Inner highlight
        self.canvas.create_oval(cx - r + 6, cy - r + 6,
                                cx - r + 14, cy - r + 14,
                                fill="#aaaaaa", outline="")

        # Status text
        label = {"sleeping": "", "listening": "Listening...",
                 "thinking": "Thinking...", "speaking": "Speaking..."}.get(self.state, "")
        if label:
            self.canvas.create_text(110, 25, text="PRAGYA",
                                    fill=color, font=("Segoe UI", 8, "bold"))
            self.canvas.create_text(110, 45, text=label,
                                    fill="#cccccc", font=("Segoe UI", 9))

        # Command text
        cmd = self.text_var.get() if self.text_var else ""
        if cmd:
            # truncate
            if len(cmd) > 22:
                cmd = cmd[:22] + "..."
            self.canvas.create_text(110, 62, text=cmd,
                                    fill="#888888", font=("Segoe UI", 8))

        self.root.after(33, self._animate)  # ~30fps

    def _blend(self, hex_color, alpha):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"#{r:02x}{g:02x}{b:02x}"

    def set_state(self, state, text=""):
        self.state = state
        if self.text_var:
            self.text_var.set(text)

    def show_command(self, text):
        if self.text_var:
            self.text_var.set(text)
            # Clear after 4 seconds
            threading.Timer(4.0, lambda: self.text_var.set("")).start()

_orb = OrbWindow()

def start_orb():
    _orb.start()

def set_orb_state(state, text=""):
    _orb.set_state(state, text)

def show_orb_command(text):
    _orb.show_command(text)
