from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

while True:
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)
    time.sleep(1)
