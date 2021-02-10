import os
import sys
import cv2
import time
import random
import imutils
import keyboard
import keys as k
import numpy as np
from PIL import ImageGrab
import pydirectinput as pdi
from PIL import Image, ImageOps

os.chdir('dataset')

np.set_printoptions(threshold = sys.maxsize)

keys = k.Keys()
say = 0

global soltara
soltara = 127
global sagtara
sagtara = 128
global tarayukseklik
tarayukseklik = 70

def tara():
    '''
    global sagtara
    sagtara = 128
    global soltara
    soltara = 128
    pixel = img[30, sagtara]
    '''

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

    '''
    while sagtara < 255:
        pixel = img[tarayukseklik, sagtara]
        if pixel == 0:
            sagtara = sagtara + 1
        else:
            break

    while soltara > 1:
        pixel = img[tarayukseklik, soltara]
        if pixel == 0:
            soltara = soltara - 1
        else:
            break
    '''
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

    img = img[int(height / 6):int((height / 6) * 4), int((width / 8) * 2):int((width / 8) * 6)]
    height, width = img.shape
    img = img[int((height / 8) * 4):height, 0:width]
    img = cv2.resize(img, (128,128))


    kernel = np.ones((3,3),np.uint8)
    img = cv2.dilate(img,kernel,iterations = 5)
    ret,img = cv2.threshold(img,240,255,cv2.THRESH_BINARY)


    if say > 50:
        tara()


    say = say + 1

    #cikti = cv2.line(img,(soltara, tarayukseklik), (sagtara, tarayukseklik), (255, 255, 255), 1)
    #orta = int((soltara + sagtara) / 2)
    #sapma = int(((64 - orta) - int(pdi.position()[0] / 10)) / 3) * -1
    #sapma = int((int((pdi.position()[0] / 10) * 2) - orta) / 4) * -1
    #cikti = cv2.line(cikti,(orta, tarayukseklik), (sapma + 128, 256), (255, 255, 255), 1)
    print(pdi.position()[0])
    #print(orta, sapma)

    if say > 10:
        if keyboard.is_pressed('n'):
            #ret,imgw = cv2.threshold(img,240,1,cv2.THRESH_BINARY)
            imgw = cv2.resize(img, (16, 16))
            isim = str(pdi.position()[0]) + '_' + str(time.time()) + '.png'
            cv2.imwrite(isim, imgw)

            with open('foo.csv', 'a') as f:
                     f.write('dataset/' + isim + ',' + str(pdi.position()[0]) + '\n')
                     f.close()

            print('yaz')


    # Display the resulting frame
    #cikti = cv2.resize(cikti, (256, 256))
    img = cv2.resize(img, (256, 256))
    cv2.imshow('wow',img)    #cv2.imshow('wow2',araba)

    if sagtara == 256:
        sagtara = 128

    if soltara == 0:
        soltara = 128

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
