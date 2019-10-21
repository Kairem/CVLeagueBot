import cv2
import numpy
from mss import mss
from PIL import Image
from pynput.mouse import Button, Controller
from pynput import keyboard
import time

#images = "C:\\Users\\eiver\\Documents\\Bots\\CVLeagueBot\\Images\\"
#playGame = images + "Playgame.jpg"
imageReadMode = 0
menuSequence = [
    cv2.imread("Images/PlayGame.jpg", imageReadMode),
    cv2.imread("Images/coopvsaibutton.png", imageReadMode),
    cv2.imread("Images/beginnerop.png", imageReadMode),
    cv2.imread("Images/confirm.png", imageReadMode),
    cv2.imread("Images/findmatch.png", imageReadMode),
    #cv2.imread("Images/accept.png", imageReadMode)
]
uisnip = cv2.imread("Images/uisnip2.png", imageReadMode)
enemyuisnipshort = cv2.imread("Images/enemyuisnipshort.png", imageReadMode)
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
    #return img

def matchTemplate (img_g, temp, threshhold = .5):
    r = cv2.matchTemplate(img_g, temp, cv2.TM_CCOEFF_NORMED)
    matches = numpy.where(r >= threshhold)
    return matches #returns matching array

def tpToImage(template, offsetX, offsetY):
    matches = matchTemplate(screenCap(), template, .9)
    if numpy.shape(matches)[1] < 1:
        return
    x = matches[1][0] + offsetX# + 75
    y = matches[0][0] + offsetY# + 20
    mc.position = (x, y)
    return True
    time.sleep(.5)

def getCoords(template, offsetX = 0, offsetY = 0):
    matches = matchTemplate(screenCap(), template, .9)
    if numpy.shape(matches)[1] < 1:
        return 0
    x = matches[1][0] + offsetX# + 75
    y = matches[0][0] + offsetY# + 20
    return (x, y)

#So i can exit without mouse control
esc = False
def on_press(key):
    if key == keyboard.Key.esc:
        global esc
        esc = True

listener = keyboard.Listener(on_press = on_press)
listener.start()

def distance(a, b, x, y):
    return abs(a-x/b-y)
step = 0
kitingDistance = 90
enemyPos = (0,0)
while(not esc):
    enemyPos = getCoords(enemyuisnipshort, 75, 130)
    if enemyPos != 0:
        #if distance(960, 540, enemyPos[0], enemyPos[1]) > kitingDistance:
            #mc.position = (1260, 240)
        #else:
        mc.position = enemyPos
        mc.press(Button.right)
        mc.release(Button.right)

    #tpToImage(uisnip, 75, 130) #offsets to roughly the center of ashes hitbox
    #time.sleep(1/60.0)
    '''if step >= len(menuSequence):
        break

    if tpToImage(menuSequence[step], 75, 20):
        step += 1
        mc.press(Button.left)
        mc.release(Button.left)
    time.sleep(0.1)'''