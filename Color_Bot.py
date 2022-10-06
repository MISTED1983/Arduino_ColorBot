import cv2
from mss import mss
import numpy as np
import win32api
import serial
import os
import pyautogui
import time
import random
from random import randrange
import keyboard
cmd = 'mode 40,20'
os.system(cmd)




arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)
arduino.close()
if not arduino.isOpen():
    arduino.open()
fov = int(input("FOV: "))
xspdd = float(input("X SPEED: "))
yspdd = float(input("Y SPEED: "))
xspd = xspdd / 10
yspd = yspdd / 10

hinput = int(input("HEAD OFFSET: "))
offset = hinput

aimass = int(input("AIMASSIST(1/0): "))  
if aimass == 1:
    xrep = 0x02
else:
    xrep =  0x01



print()
print("ACTIVE")

sct = mss()


lower = np.array([140,111,160])
upper = np.array([148,154,194])
screenshot = sct.monitors[1]
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = fov/2

def mousemove(x,y):
    if x < 0: 
        x = x+256
    if y < 0:
        y = y+256 
 
    pax = [int(x),int(y)]
    arduino.write(pax)
 

while True:
   if win32api.GetAsyncKeyState(0x01) < 0 or win32api.GetAsyncKeyState(xrep) < 0 :
        img = np.array(sct.grab(screenshot))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower,upper)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            M = cv2.moments(thresh)
            point_to_aim = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            closestX = point_to_aim[0]
            closestY = point_to_aim[1]
            diff_x = int(closestX - center)
            diff_y = int(closestY - center)
            target_x = diff_x * xspd
            target_y = diff_y * yspd
            new_target_y = target_y - offset
            mousemove(target_x, new_target_y)

            

         
         
             
