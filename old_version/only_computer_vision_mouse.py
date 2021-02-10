import cv2
import time
import random
import imutils
import keys as k
import numpy as np
from PIL import ImageGrab
import pydirectinput as pdi
from PIL import Image, ImageOps
from transform import four_point_transform

keys = k.Keys()
say = 0

global soltara
soltara = 127
global sagtara
sagtara = 128
global tarayukseklik
tarayukseklik = 70

def tara():
    global sagtara
    sagtara = 128
    global soltara
    soltara = 128
    pixel = img[30, sagtara]

    minLineLength = 5
    maxLineGap = 5
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
                if mesafe < 20 and dikmesafe > -15 and dikmesafe < 30:
                    cv2.line(img,list1[i],list2[q],(255,255,255),2)

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

    kirp = np.float32([(int((width / 8) * 3), int((height / 8) * 3)), (int((width / 8) * 5),
                                                                       int((height / 8) * 3)),
                       (int((width / 8) * 1), int((height / 8) * 6)), (int((width / 8) * 7), int((height / 8) * 6))])
    dest = np.float32([[0, 0], [256, 0], [0, 128], [256, 128]])
    matrix = cv2.getPerspectiveTransform(kirp, dest)
    #img = img[int(height / 6):int((height / 6) * 4), int((width / 8) * 2):int((width / 8) * 6)]
    #height, width = img.shape
    #img = img[int((height / 8) * 4):height, 0:width]
    img = cv2.warpPerspective(img, matrix, (256, 128))
    #img = cv2.resize(img, (256,128))

    kernel = np.ones((5,2),np.uint8)
    img = cv2.dilate(img,kernel,iterations = 7)

    if say > 50:
        tara()

    if say == 200:
        print('\a')

    say = say + 1

    cikti = cv2.line(img,(soltara, tarayukseklik), (sagtara, tarayukseklik), (255, 255, 255), 1)
    orta = int((soltara + sagtara) / 2)
    #sapma = int(((64 - orta) - int(pdi.position()[0] / 10)) / 3) * -1
    sapma = int((int((pdi.position()[0] / 10) * 2) - orta) / 4) * -1
    cikti = cv2.line(cikti,(orta, tarayukseklik), (sapma + 128, 256), (255, 255, 255), 1)
    #print(pdi.position()[0], sapma)
    print(orta, sapma)

    if say > 50:
        if soltara < 5 or sagtara > 253:
            print("kesik serit")
        elif soltara == 128 and sagtara == 128:
            if tarayukseklik < 118:
                tarayukseklik = tarayukseklik + 10
        else:
            keys.directMouse(sapma, 0)
            if tarayukseklik > 70:
                tarayukseklik = tarayukseklik - 5

        #self centering
        if pdi.position()[0] > 640:
            keys.directMouse(-3, 0)
        elif pdi.position()[0] < 640:
            keys.directMouse(3, 0)

    # Display the resulting frame
    cikti = cv2.resize(cikti, (256, 128))
    cv2.imshow('wow',cikti)
    #cv2.imshow('wow2',araba)

    if sagtara == 256:
        sagtara = 128

    if soltara == 0:
        soltara = 128

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
