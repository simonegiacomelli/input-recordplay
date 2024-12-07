from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
import time
from functools import partial
from pathlib import Path
from threading import Thread, Event

from pynput import mouse
from pynput import keyboard
from pynput.keyboard import KeyCode, Key

from irplib import extension

stop_key = 'F11'
print(f'Starting cnee recording, press {stop_key} to stop it.')

video_dir = subprocess.check_output('xdg-user-dir VIDEOS'.split(' ')).decode().strip()
dt = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
video_path = Path(video_dir)
file = video_path / f'{dt}.{extension}'
last = video_path / f'last.{extension}'

file.touch(exist_ok=False)

last_event = time.monotonic_ns()


def append(line: str):
    with open(file, 'a') as f:
        f.write(line + '\n')


stop_event = Event()


def handler(prefix: str, *args):
    global last_event
    now = time.monotonic_ns()
    delay = now - last_event
    last_event = now
    join = ','.join(map(str, args))
    append(f'{prefix},{join},{delay}')


def keyboard_handler(prefix: str, key: Key | KeyCode):
    if isinstance(key, Key):
        key = key.name
    handler(prefix, key)


def on_release(key: Key | KeyCode):
    if key == Key.f11:
        print(f'{stop_key} pressed, exiting...')
        keyboard_listener.stop()
        mouse_listener.stop()
        stop_event.set()
        # sys.exit(0)
        return
    keyboard_handler('kr', key)


def wrap(prefix: str):
    return partial(handler, prefix)


keyboard_listener = keyboard.Listener(on_press=partial(keyboard_handler, 'kp'), on_release=on_release)
mouse_listener = mouse.Listener(on_move=wrap('mm'), on_click=wrap('mc'), on_scroll=wrap('ms'))


def start():
    append('type,*args,delay_ns')
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()


Thread(target=start, daemon=True).start()
stop_event.wait()
shutil.copyfile(file, last)
print('Recording stopped.')
