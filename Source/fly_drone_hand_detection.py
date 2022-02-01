import cv2
from djitellopy import Tello
from cvzone.HandTrackingModule import HandDetector
import cvzone

detectorHand = HandDetector(maxHands=1)
gesture = ""

tello = Tello()
tello.connect()
print(tello.get_battery())
tello.streamoff()
tello.streamon()
# time.sleep(0.5)
# tello.takeoff()
# tello.move_up(40)
frame_read = tello.get_frame_read()
# For webcam input:
# cap = cv2.VideoCapture(0)
# w = cap.get(3)
# h = cap.get(4)
# print(w, h)

# cap.set(3, wCam)
# cap.set(4, hCam)

# 프레임 속성 받아오기
# w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print(w, h) # 640, 480

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('gstDrone3.avi',fourcc, 20.0, (1280,720))

while True:
    image = frame_read.frame
    height, width, _ = image.shape
    print(height, width)
    # _, image = cap.read()
    image = cv2.resize(image, (width//2, height//2))
    image = detectorHand.findHands(image)
    lmList, bboxInfo = detectorHand.findPosition(image)

    #print(lmList)
    print(bboxInfo)

    if lmList and detectorHand.handType() == "Right":

        handCenter = bboxInfo["center"]
        print("handCenter", handCenter)
        x, y, w, h = bboxInfo["bbox"]
        print("bb ", x,y,w,h)

        fingers = detectorHand.fingersUp()
        print(fingers)

        if fingers == [1, 1, 1, 1, 1]: # Open
            gesture = "Stop"
            tello.takeoff()
            tello.move_up(40)
        elif fingers == [0, 1, 0, 0, 0]: # Index
            gesture = "Up"
        elif fingers == [0, 1, 1, 0, 0]: # Victory
            gesture = "Down"
        elif fingers == [0, 0, 0, 0, 1]: # Pinky
            gesture = "Right"
        elif fingers == [1, 0, 0, 0, 0]: # Thumb
            gesture = "Left"
        elif fingers == [0, 0, 0, 0, 0]: # Fist
            gesture = "Land"
            tello.land()
        elif fingers == [0, 0, 1, 0, 0]: # Middle
            gesture = "Emergency"
        elif fingers == [1, 1, 0, 0, 1]: # SpiderMan
            gesture = "Flip"


        cv2.putText(image, f'{gesture}',
                    (x + 30, y - 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 6,cv2.LINE_AA )

    # out.write(image)
    cv2.imshow("Media Controller", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()