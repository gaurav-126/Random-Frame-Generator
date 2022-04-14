#imported necessary libraries
import time
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import cv2
import os
from PIL import Image
import random


def setdestination():
    global destinationpath
    destinationpath = filedialog.askdirectory()
    pathlabel.config(text=destinationpath)


def loadfile():
    global filepath, desktop
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filepath = filedialog.askopenfilename(initialdir=desktop, title='Select a file', filetypes=(
        ('Video', '*.mp4; *.mkv; *.wav;'), ('All Files', '*.*')))
    loadlabel.config(text=filepath)


def generateframe():
    # Opens the video
    vidcap = cv2.VideoCapture(filepath)

    #calculating duration frames/fps
    duration = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT) /
                   int(vidcap.get(cv2.CAP_PROP_FPS)))
    i = 0
    sec = 0
    #capture 10 images from the entire video to reduce the computing time
    frameRate = duration/10

    while(vidcap.isOpened()):
        ret, frame = vidcap.read()
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
        sec = sec + frameRate
        sec = round(sec, 2)

        # This condition prevents from infinite looping
        if ret == False:
            break
        
        
        interface.after(100)
        
        # Save Frame by Frame into disk using imwrite method
        cv2.imwrite(os.path.join(destinationpath,
                    'Frame'+str(i)+'.jpg'), frame)

        i += 1
        
        # if i==10:
        #     progress.stop()
    
    vidcap.release()
    cv2.destroyAllWindows()

def progressincrement():
    for i in range(0,12):
        progress['value'] +=i+1
    completelabel.configure(text = 'DONE !')
        
    
def displayframes():
    files = os.listdir(destinationpath)
    #Displaying Random 5 images from the generated frames
    for _ in range(5):
        d = random.choice(files)
        file = destinationpath+'\\'+d
        Image.open(file).show()


#Tkinter
interface = Tk()
style = ttk.Style()

interface.title('Random Frame Generator')
interface.config(background="#253B2A")
interface.resizable(width=FALSE, height=FALSE)
interface.geometry('700x400')

mainframe = Frame(interface,background='#89D99D')
frame1 = Frame(mainframe,background="#89D99D")
frame2 = Frame(mainframe,background="#89D99D")
frame3 = Frame(mainframe,background="#89D99D")

lab1 = Label(mainframe, text='Select File and Destination folder',
             bg='#89D99D', fg='#0B2B40', font=('Arial', 20), height=2)

button1 = ttk.Button(frame1, text='Browse', command=loadfile, width=10)
loadlabel = Label(frame1, width=70, anchor=W,borderwidth=1,relief=SOLID)
button2 = ttk.Button(frame1, text='Destination', command=setdestination, width=10)
pathlabel = Label(frame1, width=70, anchor=W,borderwidth=1,relief=SOLID)


lab2 = Label(mainframe, text='Generate frames from the uploaded video',
             bg='#89D99D', fg='#0B2B40', font=('Arial', 14), height=2)

button3 = ttk.Button(frame2, text='Generate Frames', command=lambda:([generateframe(),progressincrement()]))
progress = ttk.Progressbar(frame2, orient=HORIZONTAL,
                           length=300, mode='determinate',maximum=66)
completelabel = Label(frame2,bg='#89D99D', fg='#0B2B40', font=('Arial', 10))

button4 = ttk.Button(frame3, text='Display Frames', command=displayframes)
button5 = ttk.Button(frame3, text='Exit', command=interface.destroy)

#Packing all the widgets in the gui
mainframe.pack(pady = 50)
lab1.pack(fill="x")

frame1.pack(fill=BOTH)
button1.grid(row=0, column=0, pady=2,padx=(10,0))
loadlabel.grid(row=0, column=1, sticky=W, pady=2, padx=(10, 10))
button2.grid(row=1, column=0, pady=2,padx=(10,0))
pathlabel.grid(row=1, column=1, sticky=W, pady=2, padx=(10, 10))

lab2.pack(fill="x")

frame2.pack()
button3.grid(row=0, column=0, pady=2)
progress.grid(row=0, column=1, sticky=W, pady=2, padx=(10, 0))
completelabel.grid(row=0, column=2, pady=2)

frame3.pack()
button4.pack(pady=10)
button5.pack(pady=(0,20))


interface.mainloop()
