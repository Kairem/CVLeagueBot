from MouseController import MouseController
from pynput import keyboard
import time
import math
import cv2

esc = False
mc = MouseController()
print('hi')

#print(format(mc.mouse.position))
def on_press(key):
    if key == keyboard.Key.esc:
        global esc
        esc = True

listener = keyboard.Listener(on_press = on_press)
listener.start()

while (not esc):
    #print(mc.mouse.position)
    print(esc)
    mc.mouse.position = (300*math.sin(time.clock()*2) + 800, 20*math.cos(time.clock()*2) + 200)
    time.sleep(1/60.0)