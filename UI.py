from tkinter import *
import tkinter as tk
import sqlite3
import time
#from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter.filedialog import askopenfile

filename = ''

def open_file():
    global filename
    f_types = [('Jpg Files', '*.jpg')]
    file_path = filedialog.askopenfilename(title='Open a file',initialdir='/',filetypes=f_types)
    filename = file_path
    file1 = open("myfile.txt", 'w')
    file1.write(file_path)
 
    #print(filename)
    if file_path is not None:
        pass
    
#==============================METHODS========================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")       
    cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = '0000'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', '0000')")
        conn.commit()
        

def Login(event=None):
    Database()
    global Login_Flag
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            HomeWindow()
            Login_Flag = 1
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
            
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            Login_Flag = 0
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    conn.close()
 

def HomeWindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Vehicle Management System")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = Label(Home, text="Successfully Login!", font=('times new roman', 20)).pack()
    
    btn_close = Button(Home, text='Proceed', command=close).pack(pady=20, fill=X)
    btn_back = Button(Home, text='Back', command=Back).pack(pady=20, fill=X)
 
    
def close():
   Home.quit()
   Home.destroy()
 
 
def Back():
    Home.destroy()
    root.deiconify()        
    

root = Tk()
root.title("Visitor management System")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()
 
#==============================FRAMES=========================================
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)
 
#==============================LABELS=========================================
lbl_title = Label(Top, text = "Visitor management System", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)

#==============================ENTRY WIDGETS==================================
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)
 
#==============================BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=Login)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', Login)


#==============================INITIALIATION==================================

global Login_Flag
    
root.mainloop()

ws = Tk()
ws.title('ID Verification')
ws.geometry('400x200') 
    
def close1():
   ws.quit()
   ws.destroy()

if Login_Flag == 1:
    
    adhar = Label(ws, text='Upload Government id in jpg format ')
    adhar.grid(row=0, column=0, padx=10)

    adharbtn = Button(ws, text ='Choose File', command = lambda:open_file()) 
    adharbtn.grid(row=0, column=1)
        
    close = Button(ws, text='Next...', command=lambda:close1())
    close.grid(row=3,column=4)    
    ws.mainloop() 
    
    
    
    
