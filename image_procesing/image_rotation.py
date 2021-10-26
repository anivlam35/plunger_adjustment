import tkinter
from tkinter import filedialog
import os
import cv2

root = tkinter.Tk()
root.withdraw()  # use to hide tkinter window

# This file is used to rotate clockwise each photo in a set (because when we use
# raspiCamera the best usage of pixels is taking vertical photo).
def filesmanager():
    currdir = 'os.getcwd()'
    tempdir = filedialog.askopenfilenames(parent=root, initialdir=currdir, title='Please select files',
                                          filetypes=[('JPEG / JFIF', '*.jpg'),('JPEG / JFIF', '*.JPG'), ('PNG', '*.png')])
    return tempdir

images = filesmanager()

for imname in images:

        img_raw = cv2.imread(imname, 0)
        img = cv2.rotate(img_raw, cv2.ROTATE_90_CLOCKWISE)
        
        cv2.imwrite(imname, img)
