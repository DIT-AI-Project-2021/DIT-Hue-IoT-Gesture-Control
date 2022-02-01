import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import mediapipe as mp
import tkinter as tk # Tkinter
from PIL import ImageTk, Image # Pillow
from djitellopy import Tello
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
w = cap.get(3)
h = cap.get(4)
print('w=', w, 'h=', h)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_gesture.avi', fourcc, 25.0, (1280, 720))

detectorHand = HandDetector(maxHands=1)
gesture = ""
in_flight = False

hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

# tello = Tello()
# tello.connect()
# print(tello.get_battery())

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

        if fingers == [1, 0, 1, 0, 1]:
            gesture = "TAKEOFF"
            # tello.takeoff()
            # time.sleep(3)
        elif fingers == [1, 1, 0, 1, 1]:
            gesture = "LAND"
            # tello.land()
            # time.sleep(3)
        elif fingers == [0, 1, 0, 0, 0]:
            gesture = "UP"
            # tello.move_up(40)
        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "DOWN"
            # tello.move_down(40)
        elif fingers == [1, 1, 0, 0, 1]:
            gesture = "FLIP"
            # tello.flip_right()
        elif fingers == [0, 0, 0, 0, 1]:
            gesture = "RIGHT"
            # tello.move_right(40)
        elif fingers == [1, 0, 0, 0, 0]:
            gesture = "LEFT"
            # tello.move_left(40)
        elif fingers == [0, 0, 1, 0, 0]:
            gesture = "Emergency"
            # tello.emergency()
        elif fingers == [1, 1, 0, 0, 0]:
            gesture = "FORWARD"
            # tello.move_forward(40)
        elif fingers == [0, 0, 0, 1, 1]:
            gesture = "BACK"
            # tello.move_back(40)
        elif fingers == [0, 0, 0, 0, 0]:
            gesture = "STOP"
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


