##############################
# 1. Hand Detect(Murtaza)
##############################

import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

while True:
    ret, img = cap.read()
    if ret :
        img = detector.findHands(img)

        # lmList : hand position
        lmList, bbox = detector.findPosition(img)
        print(lmList)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    else:
        print("not image")
