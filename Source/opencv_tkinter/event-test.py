from tkinter import *
from tkinter import messagebox

window = Tk()

# 버튼 클릭 이벤트 핸들러
def okClick():
    print('button clicked')

button = Button(window, text="click", command=okClick())
button.pack()
window.mainloop()