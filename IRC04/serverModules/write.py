import socket
import time
import threading
import os

# WRITE TO SERVER LOG -------------
def writetost(logtext): #writes to the scrolling stack box
    if threadClose == False:
        sLog.configure(state ='normal') #for this to work, the text area is temporarily enabled
        sLog.insert('end', "\n" + logtext) #text is inserted
        sLog.configure(state ='disabled')
        sLog.see("end")#then the text editing is disabled. This doesn't work perfectly but it'll do for now.
    
# WRITE TO CONNECTED USERS --------
def writetoCU(user): #writes to the scrolling stack box
    if threadClose == False:
        cLog.configure(state ='normal') #for this to work, the text area is temporarily enabled
        cLog.insert('end', "\n" + user) #text is inserted
        cLog.configure(state ='disabled')
        cLog.see("end")#then the text editing is disabled. This doesn't work perfectly but it'll do for now.

# REMOVE FROM CONNECTED USERS -----
def remfromCU(user):
    if threadClose == False:
        user = "\n" + user
        text = cLog.get("1.0",tkinter.END)
        text = text.replace(user, "")
        cLog.configure(state ='normal')
        cLog.delete('1.0', tkinter.END)
        cLog.insert(tkinter.END, text)
        cLog.configure(state ='disabled')
        cLog.see("end")
        

# SEND TO ALL CONNECTED CLIENTS ----
def sendAllClients(message):
    if threadClose == False:
        if len(connectionarr) == 0:
            pass #don't bother if nobody is connected
        else:
            for i in range(0, len(connectionarr)):
                connectionarr[i].sendall(bytes(doEncrypt(message), "utf-8")) #iterates through all connected clients and sends them the desired message
        
