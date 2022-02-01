import tkinter as tk # Tkinter
from PIL import ImageTk, Image # Pillow
import cv2 as cv # OpenCV
import os


# cap = cv.VideoCapture('test.avi') # VideoCapture 객체 정의
cap = cv.VideoCapture(0)

while cap.isOpened(): # cap 정상동작 확인
    ret, frame = cap.read() # 프레임이 올바르게 읽히면 ret은 True
    if not ret:
        print("프레임을 수신할 수 없습니다(스트림 끝?). 종료 중 ...")
        break
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', frame)
    if cv.waitKey(42) == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv.destroyAllWindows()



