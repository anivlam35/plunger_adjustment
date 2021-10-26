import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw() 

# This functions are used for selecting paths to template and set of source photos.
# Called by "main.py"

def filesmanager():
    currdir = 'os.getcwd()'
    tempdir = filedialog.askopenfilenames(parent=root, initialdir=currdir, title='Please select files',
                                          filetypes=[('JPEG / JFIF', '*.jpg'),('JPEG / JFIF', '*.JPG'), ('PNG', '*.png')])
    return tempdir


def filemanager():
    currdir = 'os.getcwd()'
    tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select template',
                                         filetypes=[('JPEG / JFIF', '*.jpg'), ('JPEG / JFIF', '*.JPG'), ('PNG', '*.png')])
    return tempdir

