#import csv
import cv2
import time
import random
import imutils
import numpy as np
from PIL import ImageGrab
import pydirectinput as pdi
from PIL import Image, ImageOps

say = 0

global soltara
soltara = 63
global sagtara
sagtara = 64

def tara():
    global sagtara
    sagtara = 64
    global soltara
    soltara = 64
    pixel = img[30, sagtara]

    minLineLength = 5
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
                if mesafe < 0:
                    mesafe = mesafe * -1
                if mesafe < 20:
                    cv2.line(img,list1[i],list2[q],(255,255,255),2)

    while sagtara < 127:
        pixel = img[50, sagtara]
        if pixel == 0:
            sagtara = sagtara + 1
        else:
            break

    while soltara > 1:
        pixel = img[50, soltara]
        if pixel == 0:
            soltara = soltara - 1
        else:
            break

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

    img = img[int(height / 3):int((height / 3) * 2), int((width / 8) * 2):int((width / 8) * 6)]
    height, width = img.shape
    img = img[int((height / 8) * 6):height, 0:width]

    img = cv2.resize(img, (128, 128))
    kernel = np.ones((5,2),np.uint8)
    img = cv2.dilate(img,kernel,iterations = 3)

    if say > 100:
        tara()

    if say == 200:
        print('\a')

    say = say + 1

    cikti = cv2.line(img,(soltara, 50), (sagtara, 50), (255, 255, 255), 1)
    orta = int((soltara + sagtara) / 2)
    #sure = int((64 - orta) / 100)
    #if sure < 0:
    #    sure = sure * -1

    if say > 100:
        if soltara < 5 or sagtara > 123:
            print("x")
        else:
            if orta < 60:
                pdi.press("a")
            elif orta > 68:
                pdi.press("d")

    # Display the resulting frame
    cikti = cv2.resize(cikti, (512, 512))
    cv2.imshow('wow',cikti)
    #cv2.imshow('wow2',araba)

    if sagtara == 128:
        sagtara = 64

    if soltara == 0:
        soltara = 64

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
