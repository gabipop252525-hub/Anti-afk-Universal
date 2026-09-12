import sys
import subprocess
import os
import json
import threading
import tkinter as tk
from tkinter import ttk

required_packages = ["pyautogui", "keyboard"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing automatically...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import pyautogui
import keyboard

pyautogui.FAILSAFE = False

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "ActionType": 0,
    "MouseAction": "Mouse Nudge (X)",
    "NudgePixels": 3,
    "CustomKey": "space",
    "IntervalVal": 2,
    "IntervalUnit": "Min",
    "ShortcutKey": "f6"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

class AntiAFKApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anti-AFK")
        self.root.geometry("260x215")
        self.root.resizable(False, False)
        
        self.config = load_config()
        self.is_running = False
        self.thread = None

        self.status_label = tk.Label(root, text="Status: OFF", font=("Arial", 11, "bold"))
        self.status_label.place(x=20, y=20, width=170, height=25)

        self.shortcut_label_text = tk.StringVar()
        self.update_shortcut_text()
        self.info_label = tk.Label(root, textvariable=self.shortcut_label_text)
        self.info_label.place(x=20, y=50, width=180, height=20)

        self.btn_settings = tk.Button(root, text="\u2699", font=("Segoe UI", 12), command=self.open_settings)
        self.btn_settings.place(x=200, y=18, width=30, height=30)

        self.btn_on = tk.Button(root, text="ON", bg="lightgreen", command=self.start_afk)
        self.btn_on.place(x=20, y=95, width=100, height=40)

        self.btn_off = tk.Button(root, text="OFF", bg="lightcoral", command=self.stop_afk)
        self.btn_off.place(x=125, y=95, width=100, height=40)

        self.register_hotkey()

    def update_shortcut_text(self):
        self.shortcut_label_text.set(f"Shortcut: [{self.config.get('ShortcutKey', 'f6').upper()}]")

    def register_hotkey(self):
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        
        hotkey = self.config.get("ShortcutKey", "f6").strip().lower()
        if not hotkey:
            hotkey = "f6"
            
        try:
            keyboard.add_hotkey(hotkey, self.toggle_afk_from_hotkey)
        except Exception as e:
            print(f"Failed to bind hotkey '{hotkey}': {e}")

    def toggle_afk_from_hotkey(self):
        if self.is_running:
            self.root.after(0, self.stop_afk)
        else:
            self.root.after(0, self.start_afk)

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Custom Settings")
        settings_win.geometry("335x330")
        settings_win.resizable(False, False)
        settings_win.grab_set()

        tk.Label(settings_win, text="Action Type:").place(x=20, y=22, width=110, height=20)
        combo_mode = ttk.Combobox(settings_win, values=["Mouse Action", "Keyboard Key"], state="readonly")
        combo_mode.place(x=140, y=20, width=155, height=22)
        combo_mode.current(self.config["ActionType"])

        tk.Label(settings_win, text="Mouse Action:").place(x=20, y=57, width=110, height=20)
        combo_mouse = ttk.Combobox(settings_win, values=["Mouse Nudge (X)", "Mouse Nudge (Y)", "Left Click", "Right Click"], state="readonly")
        combo_mouse.place(x=140, y=55, width=155, height=22)
        if self.config["MouseAction"] in combo_mouse['values']:
            combo_mouse.set(self.config["MouseAction"])
        else:
            combo_mouse.current(0)

        tk.Label(settings_win, text="Nudge Pixels:").place(x=20, y=92, width=110, height=20)
        num_pixels = tk.Spinbox(settings_win, from_=-500, to=500)
        num_pixels.place(x=140, y=90, width=155, height=22)
        num_pixels.delete(0, tk.END)
        num_pixels.insert(0, str(self.config["NudgePixels"]))

        tk.Label(settings_win, text="Custom Key:").place(x=20, y=127, width=110, height=20)
        combo_key = ttk.Combobox(settings_win, values=["space", "w", "a", "s", "d", "shift", "ctrl", "enter", "tab"])
        combo_key.place(x=140, y=125, width=155, height=22)
        combo_key.set(self.config["CustomKey"])

        tk.Label(settings_win, text="Interval:").place(x=20, y=162, width=110, height=20)
        num_interval = tk.Spinbox(settings_win, from_=1, to=2000000)
        num_interval.place(x=140, y=160, width=80, height=22)
        num_interval.delete(0, tk.END)
        num_interval.insert(0, str(self.config["IntervalVal"]))

        combo_unit = ttk.Combobox(settings_win, values=["ms", "Sec", "Min", "Hour"], state="readonly")
        combo_unit.place(x=225, y=160, width=70, height=22)
        if self.config["IntervalUnit"] in combo_unit['values']:
            combo_unit.set(self.config["IntervalUnit"])
        else:
            combo_unit.current(1)

        tk.Label(settings_win, text="Toggle Hotkey:").place(x=20, y=197, width=110, height=20)
        entry_shortcut = tk.Entry(settings_win)
        entry_shortcut.place(x=140, y=195, width=155, height=22)
        entry_shortcut.insert(0, self.config.get("ShortcutKey", "f6"))

        def update_states(event=None):
            if combo_mode.current() == 0:
                combo_mouse.config(state="readonly")
                num_pixels.config(state="normal")
                combo_key.config(state="disabled")
            else:
                combo_mouse.config(state="disabled")
                num_pixels.config(state="disabled")
                combo_key.config(state="normal")

        combo_mode.bind("<<ComboboxSelected>>", update_states)
        update_states()

        def save_and_close():
            self.config["ActionType"] = combo_mode.current()
            self.config["MouseAction"] = combo_mouse.get()
            try:
                self.config["NudgePixels"] = int(num_pixels.get())
            except ValueError:
                pass
            self.config["CustomKey"] = combo_key.get().strip().lower()
            try:
                self.config["IntervalVal"] = int(num_interval.get())
            except ValueError:
                pass
            self.config["IntervalUnit"] = combo_unit.get()
            
            new_shortcut = entry_shortcut.get().strip().lower()
            if new_shortcut:
                self.config["ShortcutKey"] = new_shortcut

            save_config(self.config)
            self.update_shortcut_text()
            self.register_hotkey()
            settings_win.destroy()

        btn_done = tk.Button(settings_win, text="Done", command=save_and_close)
        btn_done.place(x=110, y=245, width=100, height=30)

    def start_afk(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Status: RUNNING", fg="darkgreen")
            self.btn_settings.config(state="disabled")
            
            self.thread = threading.Thread(target=self.run_loop, daemon=True)
            self.thread.start()

    def stop_afk(self):
        if self.is_running:
            self.is_running = False
            self.status_label.config(text="Status: OFF", fg="black")
            self.btn_settings.config(state="normal")

    def run_loop(self):
        val = self.config["IntervalVal"]
        unit = self.config["IntervalUnit"]
        
        multipliers = {
            "ms": 0.001,
            "Sec": 1.0,
            "Min": 60.0,
            "Hour": 3600.0
        }
        delay = val * multipliers.get(unit, 1.0)
        if delay < 0.02:
            delay = 0.02

        while self.is_running:
            start_time = time.time()
            try:
                if self.config["ActionType"] == 0:
                    action = self.config["MouseAction"]
                    pixels = self.config["NudgePixels"]
                    if action == "Mouse Nudge (X)":
                        pyautogui.moveRel(pixels, 0, duration=0.1)
                        pyautogui.moveRel(-pixels, 0, duration=0.1)
                    elif action == "Mouse Nudge (Y)":
                        pyautogui.moveRel(0, pixels, duration=0.1)
                        pyautogui.moveRel(0, -pixels, duration=0.1)
                    elif action == "Left Click":
                        pyautogui.click(button='left')
                    elif action == "Right Click":
                        pyautogui.click(button='right')
                else:
                    key = self.config["CustomKey"]
                    pyautogui.press(key if key else "space")
            except Exception as e:
                print(f"Execution error: {e}")

            while self.is_running and (time.time() - start_time) < delay:
                time.sleep(0.05)

if __name__ == "__main__":
    root = tk.Tk()
    app = AntiAFKApp(root)
    root.mainloop()