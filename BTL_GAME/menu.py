from tkinter import *
from tkinter import filedialog
import os

menu =Tk()
menu.geometry("800x660")
menu.title("NHÓM 1")
bg=PhotoImage(file='C:/Users/nguye/OneDrive/Desktop/BTL_GAME/images/menu.png')
my_label = Label(menu, image=bg)
my_label.place(x=0,y=0,relwidth=1,relheight=1)

my_frame= Frame(menu,bg="#563b34")
# my_frame.pack(pady=240)
my_frame.grid(row=0,column=0,pady=300,padx=340)

def open_Program1():
    os.system('C:/Users/nguye/OneDrive/Desktop/BTL_GAME/tank.py')
def open_Program2():
    os.system('C:/Users/nguye/OneDrive/Desktop/BTL_GAME/pvp.py')
def open_Program3():
    os.system('C:/Users/nguye/OneDrive/Desktop/BTL_GAME/images/huong_dan.txt')

menu1 = Button(my_frame, text="Chơi với máy",padx=5,command = open_Program1,bg="#563b34",fg="white",font=("iCiel Crocante",10))#"padx" chiều dài nút my_frame, "pady" chiều rộng nút my_frame
menu1.grid(row=1,column=0,pady=10) #"pady=20" khoảng trắng so với menu2
menu2 = Button(my_frame, text="Chế độ PvP", padx=5,command = open_Program2,bg="#563b34",fg="white",font=("iCiel Crocante",10))
menu2.grid(row=2,column=0,pady=10)
menu3 = Button(my_frame, text="Hướng dẫn", padx=5,command = open_Program3,bg="#563b34",fg="white",font=("iCiel Crocante",10))  
menu3.grid(row=3,column=0,pady=10)

menu.mainloop()
