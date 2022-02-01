from tkinter import *
from djitellopy import Tello
import time

# tello = Tello()
# tello.connect()

def tello_takeoff():
    print("teke-off button pressed")
    # tello.takeoff()
    # time.sleep(5)

def tello_land():
    print("land button pressed")
    # tello.land()

def process():
    print("button pressed")

window = Tk()
# btn1 = Button(window, text="Click1 me!", command=tello_takeoff())
# btn2 = Button(window, text="Click2 me!", command=tello_land())
btn3 = Button(window, text="Click3 me!", command=process())
# btn1.pack()
# btn2.pack()
btn3.pack()

window.mainloop()