import time

from pynput.keyboard import Key, Controller

keyboard = Controller()
time.sleep(0.5)
# Press and release space
keyboard.press(Key.shift)
keyboard.release(Key.shift)

keyboard.press(Key.shift)
keyboard.release(Key.shift)
