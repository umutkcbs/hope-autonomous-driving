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

global olmasi_gereken
olmasi_gereken = 640

def model_mouse_x_hesapla(img):
    #img = cv2.imread('al.png', 0)
    #print(img.shape)
    img = img.reshape(16, 16, 1)
    img = np.expand_dims(img, axis=0)
    #print(img.shape)
    pred = model.predict(img)
    #print(pred)
    sonuc = np.nonzero(pred == 1)
    mousex = sonuc[1] + 615
    try:
        mousex = mousex[0]
    except Exception as e:
        mousex = 640
        print("------err------")
    return mousex


def tara():
    minLineLength = 1
    maxLineGap = 1
    lines = cv2.HoughLinesP(img,1,np.pi/180,100,minLineLength,maxLineGap)
    if lines is not None:
        list1 = []
        list2 = []

        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                list1.append((x1,y1))
                list2.append((x2,y2))

            for i in range(0, int(len(list1) / 2)):
                sequence = [i for i in range(0, len(list2))]
                q = random.choice(sequence)
                mesafe = list1[i][0] - list2[q][0]
                dikmesafe = list1[i][1] - list2[q][1]
                if mesafe < 0:
                    mesafe = mesafe * -1
                if mesafe < 20 and dikmesafe > -35 and dikmesafe < 50:
                    cv2.line(img,list1[i],list2[q],(255,255,255),5)

while(True):
    global img
    global gray
    # Capture frame-by-frame
    img = ImageGrab.grab(bbox=(0,0,1280,720)) #ets tam ekran
    img = np.array(img)

    height, width, channels = img.shape

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 5)
    img = cv2.Canny(img, 100, 200)

    #roi
    img = img[int(height / 6):int((height / 6) * 4), int((width / 8) * 2):int((width / 8) * 6)]
    height, width = img.shape
    img = img[int((height / 8) * 4):height, 0:width]
    img = cv2.resize(img, (128,128))


    kernel = np.ones((3,3),np.uint8)
    img = cv2.dilate(img,kernel,iterations = 5)
    ret,img = cv2.threshold(img,240,255,cv2.THRESH_BINARY)

    if say > 50:
        tara()

    if say == 50:
        pygame.mixer.Sound.play(bip)

    say = say + 1

    print(pdi.position()[0], olmasi_gereken)

    if say > 50:
        if keyboard.is_pressed('f4') == False:
            #ret,imgw = cv2.threshold(img,240,1,cv2.THRESH_BINARY)
            img = cv2.resize(img, (16, 16))
            olmasi_gereken = model_mouse_x_hesapla(img)
            sapma = int(pdi.position()[0] - olmasi_gereken) * -1
            keys.directMouse(sapma, 0)
        else:
            pygame.mixer.Sound.play(bip)
            print('------  ||  ------')
            break
            #time.sleep(10)
            #print('------  |>  ------')
            #pygame.mixer.Sound.play(bip)


    # Display the resulting frame
    img = cv2.resize(img, (256, 256))
    cv2.imshow('wow',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
