import tkinter as tk # Tkinter
import cv2
from PIL import ImageTk, Image # Pillow
import cv2 as cv # OpenCV
import os

from djitellopy import Tello
import time

from cvzone.HandTrackingModule import HandDetector
import cvzone

detectorHand = HandDetector(maxHands=1)
gesture = ""

# For webcam input:
# cap = cv2.VideoCapture(0)

# tello = Tello()
# tello.connect()

# def tello_connect():
#     print("Connect to Tello Drone")
#     tello.connect()
#
#     battery_level = tello.get_battery()
#     print(f"Battery Life Percentage: {battery_level}")

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('out.avi',fourcc, 20.0, (640,480))

def tello_takeoff():
    print("teke-off button pressed")
    # tello.takeoff()
    # time.sleep(3)

def tello_land():
    print("land button pressed")
    # tello.land()

# GUI 설계
win = tk.Tk() # 인스턴스 생성

win.title("AI Drone Controller") # 제목 표시줄 추가
win.geometry("920x640+50+50") # 지오메트리: 너비x높이+x좌표+y좌표
win.resizable(False, False) # x축, y축 크기 조정 비활성화

# 라벨 추가
lbl = tk.Label(win, text="AI Drone Controller")
lbl.grid(row=0, column=0) # 라벨 행, 열 배치

# 버튼 추가
btnTakeOff = tk.Button(win, text="take-off", command=tello_takeoff)
btnTakeOff.grid(row=0, column=1)

btnLand = tk.Button(win, text="land", command=tello_land)
btnLand.grid(row=0, column=2)


# 프레임 추가
frm = tk.Frame(win, bg="white", width=720, height=480) # 프레임 너비, 높이 설정
frm.grid(row=1, column=0) # 격자 행, 열 배치

# 라벨1 추가
lbl1 = tk.Label(frm)
lbl1.grid(row=0, column=0)

cap = cv.VideoCapture(0) # VideoCapture 객체 정의

def video_play():
    ret, frame = cap.read() # 프레임이 올바르게 읽히면 ret은 True
    if not ret:
        cap.release() # 작업 완료 후 해제
        return

    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # frame = cv.resize(frame, (360, 240))

    ########################
    image = detectorHand.findHands(frame)
    lmList, bboxInfo = detectorHand.findPosition(image)

    # print(lmList)
    print("bbboxInfo", bboxInfo)

    if lmList and detectorHand.handType() == "Right":

        handCenter = bboxInfo["center"]
        print("handCenter", handCenter)
        x, y, w, h = bboxInfo["bbox"]
        print("bb ", x, y, w, h)

        fingers = detectorHand.fingersUp()
        print(fingers)

        if fingers == [1, 1, 1, 1, 1]:  # Open
            gesture = "Stop"
        elif fingers == [0, 1, 0, 0, 0]:  # Index
            gesture = "Up"
        elif fingers == [0, 1, 1, 0, 0]:  # Victory
            gesture = "Down"
        elif fingers == [0, 0, 0, 0, 1]:  # Pinky
            gesture = "Right"
        elif fingers == [1, 0, 0, 0, 0]:  # Thumb
            gesture = "Left"
        elif fingers == [0, 0, 0, 0, 0]:  # Fist
            gesture = "Land"
        elif fingers == [0, 0, 1, 0, 0]:  # Middle
            gesture = "Emergency"
        elif fingers == [1, 1, 0, 0, 1]:  # SpiderMan
            gesture = "Flip"
        else:
            gesture = ""

        cv2.putText(image, f'{gesture}',
                    (x + 30, y - 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 6, cv2.LINE_AA)

    img = Image.fromarray(image) # Image 객체로 변환
    imgtk = ImageTk.PhotoImage(image=img) # ImageTk 객체로 변환
    # OpenCV 동영상
    lbl1.imgtk = imgtk
    lbl1.configure(image=imgtk)
    lbl1.after(10, video_play)

    # 동영상 저장
    out.write(frame)

video_play()

# tello_connect()

win.mainloop() #GUI 시작