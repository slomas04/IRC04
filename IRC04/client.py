###  _____ _____   _____ ___  _  _   
### |_   _|  __ \ / ____/ _ \| || |  
###   | | | |__) | |   | | | | || |_ 
###   | | |  _  /| |   | | | |__   _|
###  _| |_| | \ \| |___| |_| |  | |  
### |_____|_|  \_\\_____\___/   |_|  
### Client
### Made by Samuel Lomas
### https://github.com/slomas04

import socket
import threading
import os
import tkinter as tk
import tkinter.scrolledtext as st

key = 'Y������)b�r��7���V�wuȬ�Xb���GJ,A8����5�Zd���cN����2�K����H�M_��R���0�WO7�� V_���X&bRa+���ϙɚK���a\������!G�,�Kb~{��ll���b�<�R6ҩ ���x}_k�����YmN������/����ٜtuLט%��[�)��VpQnr�Zd���cN�����K����H�M_��R���0�WO7�� V_���X&bRa+���ϙɚK����a\�lol'

TARGET_IP = input("Enter the server IP\n>>> ")
while True:
    try:
        TARGET_PORT = int(input("Enter the server port\n>>> "))
        break
    except:
        print("Not an Int!")

USERNAME = input("What is your username?\n>>> ")

# ENCRYPT -----------------
def doEncrypt(string):
    #string = string.upper()
    #key = key.upper()
    outString = []
    for i in range(0, len(string)):
        outString += chr((ord(string[i])) + (ord(key[i])))
    outString = "".join(outString)
    return outString

# DECRYPT -----------------
def doDecrypt(string):
    #string = string.upper()
    #key = key.upper()
    outString = []
    for i in range(0, len(string)):
        outString += chr((ord(string[i])) - (ord(key[i])))
    outString = "".join(outString)
    return outString

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket object using IPV4 and TCP respectively
rThreadRun = True

window = tk.Tk()
window.title("IRC04 Client")

text_area = st.ScrolledText(window, width = 80, height = 20, font = ("Times New Roman",13))
text_area.grid(row = 0, column = 1, pady = 2)
text_area.configure(state ='disabled')

text_entry = tk.Entry(window, width = 80, font = ("Times New Roman",13))
text_entry.grid(row = 1, column = 1, pady = 2)       

def exitRoutine():
    writetost("[CLIENT] - Shutting down now!")
    s.sendall(bytes(doEncrypt("!04exit"), "utf-8"))
    rThreadRun = False
    window.destroy()
    os._exit(1)

def utf8len(a):
    return len(a.encode('utf-8')) #returns length of string in unicode

def writetost(logtext): #writes to the scrolling stack box
    text_area.configure(state ='normal') #for this to work, the text area is temporarily enabled
    text_area.insert('end', "\n" + logtext) #text is inserted
    text_area.configure(state ='disabled')
    text_area.see("end")#then the text editing is disabled. This doesn't work perfectly but it'll do for now.

def returnPressed(event):
    if text_entry.get() == "":
        pass
    elif text_entry.get() == "!04exit": #need to actually let the user exit
        text_entry.delete(0, 'end')
        exitRoutine()

    elif text_entry.get() == "!04help": #help
        text_entry.delete(0, 'end')
        writetost("[CLIENT] - Commands:\n - !04help - Displays all commands\n - !04exit - Shuts down the server")
        
    else:
        storedtxt = text_entry.get()
        text_entry.delete(0, 'end')
        s.sendall(bytes(doEncrypt(storedtxt), "utf-8"))

def recievethread():
    while rThreadRun == True:
        full_msg = ''
        msg = s.recv(512) #waits to recieve message
        full_msg += doDecrypt(msg.decode("utf-8")) #decode
        writetost(full_msg) #print

text_entry.bind('<Return>', returnPressed)
        
s.connect((TARGET_IP, TARGET_PORT)) #establish connection on the same machine for now
s.sendall(bytes(doEncrypt(USERNAME), "utf-8"))

recieving = threading.Thread(target=recievethread)
recieving.start()

window.protocol("WM_DELETE_WINDOW", exitRoutine)
window.mainloop()
exit()