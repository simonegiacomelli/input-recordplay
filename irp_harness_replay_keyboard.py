import time

from pynput.keyboard import Key, Controller

keyboard = Controller()
time.sleep(0.5)
# Press and release space
keyboard.press(Key.cmd)
time.sleep(0.1)
keyboard.press('1')
time.sleep(0.1)
keyboard.release('1')
time.sleep(0.1)
keyboard.release(Key.cmd)

