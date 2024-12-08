import subprocess
import sys
from pathlib import Path
from time import sleep

from dotool_keys import DotoolKeys
from dotool_mapping import pynput_to_dotool_key
from irplib import get_video_path, extension

from pynput.keyboard import Key
from pynput import keyboard, mouse


class DotoolKeyboard:

    def __init__(self):
        self.process = subprocess.Popen(['dotool'], stdin=subprocess.PIPE, text=True)
        self.dotool_keys = DotoolKeys()

    def send(self, line: str):
        self.process.stdin.write(f'{line}\n')
        self.process.stdin.flush()

    def has_chord(self, key: str):
        return key in self.dotool_keys.keys


key_contr = DotoolKeyboard()
mouse_contr = mouse.Controller()


def process_keyboard(line, values: list[str]):
    key_str = values[1]
    keydown = values[0][1] == 'p'
    if key_str.startswith("'"):
        if keydown:  # ignore keyup
            key = key_str[1]
            key_contr.send(f'type {key}')
    else:
        key = pynput_to_dotool_key(key_str)
        if not key_contr.has_chord(key):
            print(f'unknown key: {key}')
            sys.exit(1)
        func = 'keydown' if keydown else 'keyup'
        line = f'{func} {key}'
        print(f'process_keyboard: {line}')
        key_contr.send(line)


def process_mouse(line, values: list[str]):
    print(f'process_mouse: {line}')
    event_type = values[0]
    if event_type == 'mm':
        x, y = map(int, values[1:3])
        print(f'move mouse to {x}, {y}')
        mouse_contr.position = (x, y)
    elif event_type == 'mc':
        # mc,23,1579,Button.left,True,472476012
        # mc,23,1579,Button.left,False,157801005
        x, y, button, pressed = values[1:5]
        x, y = map(int, (x, y))
        button = getattr(mouse.Button, button.removeprefix('Button.'))
        func = mouse_contr.press if pressed == 'True' else mouse_contr.release
        func(button)
    else:
        raise Exception(f'process_mouse skip: {line}')


def main():
    stop_replay = False

    def on_press(key):
        nonlocal stop_replay
        if key == Key.esc or key == Key.f11:
            print('esc pressed, exiting...')
            stop_replay = True

    keyboard.Listener(on_press=on_press).start()

    video_path = get_video_path() / f'last.{extension}'
    # process line by line in lazy
    with open(video_path) as f:
        next(f)  # skip header
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = line.split(',')
            event_type = line[0]

            delay_ns = int(values[-1])
            delay_secs = delay_ns / 1e9
            print(f'delaying {delay_secs} seconds')
            sleep(delay_secs)

            if stop_replay:
                break

            if event_type == 'k':
                process_keyboard(line, values)
            if event_type == 'm':
                process_mouse(line, values)


if __name__ == '__main__':
    main()
