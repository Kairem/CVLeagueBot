import cv2
import numpy
from mss import mss
from PIL import Image
from pynput.mouse import Button, Controller
from pynput import keyboard
import time

#images = "C:\\Users\\eiver\\Documents\\Bots\\CVLeagueBot\\Images\\"
#playGame = images + "Playgame.jpg"
menuSequence = [
    cv2.imread("Images/PlayGame.jpg", 0),
    cv2.imread("Images/coopvsaibutton.png", 0),
    cv2.imread("Images/beginnerop.png", 0),
    cv2.imread("Images/confirm.png", 0),
    cv2.imread("Images/findmatch.png", 0),
    cv2.imread("Images/accept.png", 0)
]

mc = Controller()
monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
screen = mss()
sct = 0

#Takes a screenshot and returns greyscaled img in numpy array
def screenCap():
    sct = screen.grab(monitor)
    img = Image.frombytes("RGB", sct.size, sct.rgb)
    img = numpy.array(img)
    img = img[:, :, ::-1]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray

def matchTemplate (img_g, temp, threshhold = .5):
    r = cv2.matchTemplate(img_g, temp, cv2.TM_CCOEFF_NORMED)
    matches = numpy.where(r >= threshhold)
    return matches #returns matching array

def clickButton(template):
    matches = matchTemplate(screenCap(), template, .9)
    if numpy.shape(matches)[1] < 1:
        return
    x = matches[1][0] + 75
    y = matches[0][0] + 20
    mc.position = (x, y)
    return True
    time.sleep(.5)

#So i can exit without mouse control
esc = False
def on_press(key):
    if key == keyboard.Key.esc:
        global esc
        esc = True

listener = keyboard.Listener(on_press = on_press)
listener.start()

step = 0
while(not esc):
    if step >= len(menuSequence):
        break

    if clickButton(menuSequence[step]):
        step += 1
        mc.press(Button.left)
        mc.release(Button.left)
    time.sleep(0.05)