###  _____ _____   _____ ___  _  _   
### |_   _|  __ \ / ____/ _ \| || |  
###   | | | |__) | |   | | | | || |_ 
###   | | |  _  /| |   | | | |__   _|
###  _| |_| | \ \| |___| |_| |  | |  
### |_____|_|  \_\\_____\___/   |_|  
### Server
### Made by Samuel Lomas
### https://github.com/slomas04

import socket
import time
import threading
import tkinter
import tkinter.scrolledtext as st
from tkinter import simpledialog
import os
from serverModules.encryption import doDecrypt, doEncrypt
from serverModules.write import writetost, writetoCU, remfromCU, sendAllClients 
from serverModules.clientThread import newClientThread, listenThread

# POPUPS -------------------------
popup = tkinter.Tk()
popup.withdraw()
SERVER_ADDR = simpledialog.askstring(title="Input", prompt="Enter your Local IP:")
while True:
    try:
        SERVER_PORT = int(simpledialog.askstring(title="Input", prompt="Enter your server port:"))
        break
    except:
        print("Not an Int!")
popup.destroy()


# TKINTER DEFS --------------------

root = tkinter.Tk()
root.title("IRC04 Server")

sLogLabel = tkinter.Label(root, text='Server Log:', width = 80, font = ("Times New Roman",13), anchor = 'w')
connClientsLabel = tkinter.Label(root, text='Connected Users:', width = 20, font = ("Times New Roman",13), anchor = 'w')

sLogLabel.grid(column=0, row=0)
connClientsLabel.grid(column=1, row=0)

sLog = st.ScrolledText(root, width = 80, height = 17, font = ("Times New Roman",13))
cLog = st.ScrolledText(root, width = 20, height = 17, font = ("Times New Roman",13))

sLog.grid(column=0, row=1)
cLog.grid(column=1, row=1)

entryBoxLabel = tkinter.Label(root, text='Enter commands:', width = 80, font = ('Times New Roman', 13), anchor = 'w')
entryBoxLabel.grid(column=0, row=2)

entryBox = tkinter.Entry(root, width = 105, font = ("Times New Roman",13))
entryBox.grid(column=0, row=3, columnspan = 2)

MAXBUFFER = 512

threadClose = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket object using IPV4 and TCP respectively

s.bind((SERVER_ADDR, SERVER_PORT)) #bind the server to host machine through port 

connectionarr = [] #array of all connections

s.listen(5) #listen for connections with a queue size of 10

key = "Y������)b�r��7���V�wuȬ�Xb���GJ,A8����5�Zd���cN����2�K����H�M_��R���0�WO7�� V_���X&bRa+���ϙɚK���a\������!G�,�Kb~{��ll���b�<�R6ҩ ���x}_k�����YmN������/����ٜtuLט%��[�)��VpQnr�Zd���cN�����K����H�M_��R���0�WO7�� V_���X&bRa+���ϙɚK����a\�lol"

    
            
# EXIT ROUTINE --------------------
def exitRoutine():
    writetost("[SERVER] - Shutting down now!")
    sendAllClients("[SERVER] - Shutting down now!")
    threadClose = True
    if len(connectionarr) == 0:
        pass #don't bother if nobody is connected
    else:
        for i in range(0, len(connectionarr)):
            connectionarr[i].close() #iterates through all connected clients kills the socket
    os._exit(0)
    
# RETURN PRESSED ------------------
def returnPressed(event):
    if entryBox.get() == "":
        pass
    elif entryBox.get() == "!04exit":
        exitRoutine()
    else:
        storedtxt = entryBox.get()
        entryBox.delete(0, 'end')
        storedtxt = "[SERVER] - " + (storedtxt)
        writetost(storedtxt)
        sendAllClients(storedtxt)


root.protocol("WM_DELETE_WINDOW", exitRoutine)
entryBox.bind('<Return>', returnPressed)
listening = threading.Thread(target=listenThread, args=())
listening.daemon = True
listening.start()

root.mainloop()
