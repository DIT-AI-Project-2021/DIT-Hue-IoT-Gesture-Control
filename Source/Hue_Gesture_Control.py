##################################
# Hue IoT Gesture Contrlo 2021.2.1
##################################
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import mediapipe as mp
import tkinter as tk # Tkinter
from PIL import ImageTk, Image # Pillow
# from djitellopy import Tello
import time
from phue import Bridge
import logging
import random
import time, threading

logging.basicConfig()
b = Bridge('192.168.0.21')

# print(b.get_api())

# Get a flat list of the light objects
lights_list = b.get_light_objects('list')
print(lights_list)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(1)
w = cap.get(3)
h = cap.get(4)
print('w=', w, 'h=', h)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('hue_gesture.avi', fourcc, 25.0, (1280, 720))

detectorHand = HandDetector(maxHands=1)
gesture = ""
in_flight = False

hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

# tello = Tello()
# tello.connect()
# print(tello.get_battery())
        
def random_color():
    for light in lights_list:
        light.brightness = 254
        light.xy = [random.random(),random.random()]

while True:
    _, img = cap.read()
    img = detectorHand.findHands(img)
    lmList, bboxInfo = detectorHand.findPosition(img)

    # bboxInfo: {'id': 20, 'bbox': (346, 7, 240, 259), 'center': (466, 136)}

    if lmList and detectorHand.handType() == "Right":

        handCenter = bboxInfo["center"]
        # print('bboxInfo: ', bboxInfo)
        x, y, w, h = bboxInfo['bbox']
        # print(x, y ,w, h)

        # bboxRegion = x - 20, y , 175, h + 25
        bboxRegion = x, y, w, h
        cvzone.cornerRect(img, bboxRegion, rt=0, t=5, colorC=(0, 255, 255))

        # # x < cx < x+w
        inside = bboxRegion[0] < handCenter[0] < bboxRegion[0] + bboxRegion[2] and \
                 bboxRegion[1] < handCenter[1] < bboxRegion[1] + bboxRegion[3]

        if inside:
            cvzone.cornerRect(img, bboxRegion, rt=0, t=3, colorC=(0, 255, 0))

        fingers = detectorHand.fingersUp()

        if fingers == [0, 0, 0, 0, 0]:  # Lamp OFF
            gesture = "Lamp OFF"
            # for light in lights_list:
            #     light.on = False
            b.set_light(7, 'on', False)
            
            # tello.takeoff()
            # time.sleep(3)
            pass
        elif fingers == [1, 1, 1, 1, 1]: # Lamp ON
            gesture = "Lamp ON"
            # for light in lights_list:
            #     light.on = True
            
            b.set_light(7, 'on', True)
            # tello.land()
            # time.sleep(3)
            pass
        elif fingers == [0, 1 , 0, 0, 0]:
            gesture = "BLUE"
            # for light in lights_list:
            #     light.brightness = 254
            #     light.xy = [0.1,0.1]
            b.lights[1].xy = [0.1, 0.1]
            # tello.move_up(40)
        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "RED"
            b.set_light(7, 'on', True)
            # for light in lights_list:
            #     light.brightness = 254
            #     light.xy = [0.7, 0.3]
            b.lights[1].xy = [0.7, 0.3]
            # tello.move_down(40)
        elif fingers == [0, 0, 1, 1, 1]:
            gesture = "YELLOW"
            b.set_light(7, 'on', True)
            # for light in lights_list:
            #     light.brightness = 254
            #     light.xy = [0.5, 1]
            b.lights[1].xy = [0.5, 1]
            # tello.flip_right()
        elif fingers == [0, 1, 1, 1, 1]:
            b.set_light(7, 'on', True)
            random_color()
            gesture = "BLINK"
            # tello.move_right(40)
        
        # elif fingers == [1, 0, 0, 0, 0]:
    
        #     # gesture = "CHANGE RGB"
        #     # tello.move_left(40)
        #     pass
        # elif fingers == [0, 0, 1, 0, 0]:
        #     # gesture = "Emergency"
        #     # tello.emergency()
        #     pass
        # elif fingers == [1, 1, 0, 0, 0]:
        #     # gesture = "FORWARD"
        #     # tello.move_forward(40)
        #     pass
        # elif fingers == [0, 0, 0, 1, 1]:
        #     # gesture = "BACK"
        #     # tello.move_back(40)
        #     pass
        # elif fingers == [0, 0, 0, 0, 0]:
        #     # gesture = "STOP"
        #     pass
        else:
            gesture = "No Gesture"

        if gesture != "No Gesture":
            cv2.rectangle(img, (bboxRegion[0], bboxRegion[1] + bboxRegion[3] + 10),
                          (bboxRegion[0] + bboxRegion[2], bboxRegion[1] + bboxRegion[3] + 60),
                          (0, 255, 0),cv2.FILLED)

            cv2.putText(img, f'{gesture}',
                        (bboxRegion[0] + 10, bboxRegion[1] + bboxRegion[3] + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    out.write(img)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        # tello.land()
        print('land')
        break
