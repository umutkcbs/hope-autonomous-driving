'''
https://github.com/umutkcbs/hope-autonomous-driving

Move game window top-left corner (or full screen) and make the steering wheel centered.
Press F1 and stop game, run the code and turn back to game. Code will take over steering control.
You must not move your mouse before code start.

Hold "Z" to pass to left lane, hold "X" to pass to right lane.
Press F1 to stop the code.
'''
import cv2
import time
import pygame
import random
import imutils
import keyboard
import keys as k
import numpy as np
import tensorflow as tf
from PIL import ImageGrab
import pydirectinput as pdi
from tensorflow import keras
from PIL import Image, ImageOps

model = keras.models.load_model('model.h5')

pygame.init()
bip = pygame.mixer.Sound('abep.mp3')

keys = k.Keys()
say = 0

start_delay = 50

global olmasi_gereken
olmasi_gereken = 640

mode = 1   #   <--0     <-1->     2-->
def model_mouse_x_hesapla(img, mode):
    #img = cv2.imread('al.png', 0)
    #print(img.shape)

    img = img.reshape(16, 16, 1)
    img = np.expand_dims(img, axis=0)
    #print(img.shape)
    pred = model.predict(img)
    #print(pred)
    sonuc = np.nonzero(pred == 1)
    if mode == 1:
        mousex = sonuc[1] + 615
    elif mode == 0:
        mousex = sonuc[1] + 605
    elif mode == 2:
        mousex = sonuc[1] + 625
    try:
        mousex = mousex[0]
    except Exception as e:
        mousex = 640
        print("------err------")
    return mousex

def filterimg(img):
    img = cv2.medianBlur(img, 5)
    img = cv2.Canny(img, 100, 200)

    img = cv2.resize(img, (128,128))

    kernel = np.ones((3,3),np.uint8)
    img = cv2.dilate(img,kernel,iterations = 5)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    ret,img = cv2.threshold(img,230,255,cv2.THRESH_BINARY)
    return img

while(True):
    global img
    global gray

    img = ImageGrab.grab(bbox=(0,0,1280,720)) #x, y, width, height  //   resolution must be 720p
    img = np.array(img)
    height, width, channels = img.shape
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #roi
    img = img[int(height / 6):int((height / 6) * 4), int((width / 8) * 2):int((width / 8) * 6)]
    #img = img[int(height / 6):int((height / 6) * 4), int((width / 8) * 3):int((width / 8) * 5)] (high fov beta)
    height, width = img.shape
    img = img[int((height / 8) * 4):height, 0:width]

    img = filterimg(img)

    #Your mouse' X coordinate, coordinate the model says
    print(pdi.position()[0], olmasi_gereken)

    say = say + 1
    if say == start_delay:
        keyboard.press_and_release('f1')
        pygame.mixer.Sound.play(bip)
    if say > start_delay:
        if keyboard.is_pressed('f1') == False:
            img = cv2.resize(img, (16, 16))
            img = cv2.rectangle(img, (0,0), (15,16), (0,0,0), 1)

            if keyboard.is_pressed('z'):
                olmasi_gereken = model_mouse_x_hesapla(img, 0)
                sapma = int(pdi.position()[0] - olmasi_gereken) * -1
                keys.directMouse(sapma, 0)
            elif keyboard.is_pressed('x'):
                olmasi_gereken = model_mouse_x_hesapla(img, 2)
                sapma = int(pdi.position()[0] - olmasi_gereken) * -1
                keys.directMouse(sapma, 0)
            else:
                olmasi_gereken = model_mouse_x_hesapla(img, 1)
                sapma = int(pdi.position()[0] - olmasi_gereken) * -1
                keys.directMouse(sapma, 0)
        else:
            pygame.mixer.Sound.play(bip)
            print('------  ||  ------')
            break

    # Display the resulting frame
    img = cv2.resize(img, (256, 256))
    cv2.imshow('wow',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()
