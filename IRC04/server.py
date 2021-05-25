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
        
# CLIENT THREAD --------------------
def newClientThread(connection, ip, port):
    try:
        connection.settimeout(1)
        welcomemsg = "[SERVER] - Welcome to the Server!\n[SERVER] - For commands, type !04help"
        connection.sendall(bytes(doEncrypt(welcomemsg), "utf-8")) #send welcome message to client
        username = connection.recv(512) #take the username from the client
        username = doDecrypt(username.decode("utf-8")) #decode
        if username == "SERVER":
            connection.close()
        writetoCU(username)
        sendAllClients("[SERVER] - User " + username + " has connected")
        while threadClose == False:
            full_msg = ''
            try:
                msg = connection.recv(1024)
            except socket.timeout:
                continue
            except:
                break
            full_msg += doDecrypt(msg.decode("utf-8")) #decode
            if threadClose == False:
                if full_msg == "!04exit":
                    writetost("[CONSOLE] - " + str(ip) + ":" + str(port) + " Username = " + username + " Has Disconnected from the server")
                    sendAllClients("[SERVER] - User " + username + " has disconnected")
                    remfromCU(username)
                    connectionarr.remove(connection)
                    connection.close()
                    break
                writetost("[CONSOLE] - " + str(ip) + ":" + str(port) + " Username = " + username + " sends: " + full_msg)
                full_msg = "[" + username + "] - " + full_msg #append tag to message
                sendAllClients(full_msg)
                
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        remfromCU(username)
        connectionarr.remove(connection)
        connection.close()

# LISTEN FOR NEW CLIENTS ----------
def listenThread():
    writetost("[CONSOLE] - Server now starting...")
    writetost("[CONSOLE] - Server listening for connections...")
    while threadClose == False: #listen for connections infinitely
        try:
            connection, address = s.accept()#when a connection is established, assign the client's socket to clientsock and IPV4 to address
            ip, port = str(address[0]), str(address[1])
            connectionarr.append(connection)
            writetost("[CONSOLE] - Connected with " + ip + ":" + port)
            threading.Thread(target=newClientThread, args=(connection, ip, port), daemon=True).start()
            
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            
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