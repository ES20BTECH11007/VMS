from tkinter import *
import tkinter as tk
import sqlite3
import time
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from os.path import exists

filename = ''


def open_file():
    global filename
    f_types = [('Jpeg Files', '*.jpeg')]
    file_path = filedialog.askopenfilename(title='Open a file',initialdir='/',filetypes=f_types)
    filename = file_path
    file1 = open("myfile.txt", 'w')
    file1.write(file_path)
 
    if file_path is not None:
        pass
    
    
ws = Tk()
ws.title('ID Verification')
ws.geometry('400x200') 
    
def close1():
   ws.quit()
   ws.destroy()


    
adhar = Label(ws, text='Upload Government id in jpg format ')
adhar.grid(row=0, column=0, padx=10)

adharbtn = Button(ws, text ='Choose File', command = lambda:open_file()) 
adharbtn.grid(row=0, column=1)
        
close = Button(ws, text='Next...', command=lambda:close1())
close.grid(row=3,column=4)    
ws.mainloop()     

if exists('myfile.txt'):
    f = open('myfile.txt', 'r')
    path = f.readline()
    print('Upload image test case passed- file_path as extracted from myfile.txt file is :', path)
else:
    print('Test case failed')    



