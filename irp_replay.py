from time import sleep

from irplib import get_video_path, extension

from pynput.keyboard import Key, Controller

keyboard = Controller()


def process_keyboard(line, values: list[str]):
    print(f'Processing line: {line}')
    delay = int(values[2])
    sleep(delay / 1_000_000_000)
    key = values[1]
    Key.f11
    func = keyboard.press if values[0][1] == 'p' else keyboard.release
    func(key)


def main():
    video_path = get_video_path() / f'last.{extension}'
    # process line by line in lazy
    with open(video_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = line.split(',')
            event_type = line[0]
            if event_type == 'k':
                process_keyboard(line, values)


if __name__ == '__main__':
    main()
