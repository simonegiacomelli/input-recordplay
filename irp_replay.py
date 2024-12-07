from time import sleep

from irplib import get_video_path, extension

from pynput.keyboard import Key, Controller
from pynput import keyboard
controller = Controller()


def process_keyboard(line, values: list[str]):
    print(f'Processing line: {line}')
    key_str = values[1]
    if key_str.startswith("'"):
        key = key_str[1]
    else:
        key = getattr(Key, key_str)
    func = controller.press if values[0][1] == 'p' else controller.release
    func(key)


def main():
    stop_replay = False

    def on_press(key):
        nonlocal stop_replay
        if key == Key.esc:
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


if __name__ == '__main__':
    main()
