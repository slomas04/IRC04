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

MAXBUFFER = 1024
SERVER_ADDR = input("Enter your local IP\n>>> ")
while True:
    try:
        SERVER_PORT = int(input("Enter the server port\n>>> "))
        break
    except:
        print("Not an Int!")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket object using IPV4 and TCP respectively

s.bind((SERVER_ADDR, SERVER_PORT)) #bind the server to host machine through port 

connectionarr = []

s.listen(5) #listen for connections with a queue size of 10

def sendAllClients(message):
    if len(connectionarr) == 0:
        pass #don't bother if nobody is connected
    else:
        for i in range(0, len(connectionarr)):
            connectionarr[i].sendall(bytes(message, "utf-8")) #iterates through all connected clients and sends them the desired message
        
def newClientThread(connection, ip, port):
    try:
        welcomemsg = "[SERVER] - Welcome to the Server!\n[SERVER] - For commands, type !04help"
        connection.sendall(bytes(welcomemsg, "utf-8")) #send welcome message to client
        username = connection.recv(1024) #take the username from the client
        username = username.decode("utf-8") #decode
        sendAllClients("[SERVER] - User " + username + " has connected")
        while True:
            full_msg = ''
            msg = connection.recv(1024)
            full_msg += msg.decode("utf-8") #decode
            if full_msg == "!04exit":
                print("[CONSOLE] - " + str(ip) + ":" + str(port) + " Username = " + username + " Has Disconnected from the server")
                sendAllClients("[SERVER] - User " + username + " has disconnected")
                connectionarr.remove(connection)
                break
            print("[CONSOLE] - " + str(ip) + ":" + str(port) + " Username = " + username + " sends: " + full_msg)
            full_msg = "[" + username + "] - " + full_msg #append tag to message
            sendAllClients(full_msg)
                
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

while True: #listen for connections infinitely
    try:
        connection, address = s.accept()#when a connection is established, assign the client's socket to clientsock and IPV4 to address
        ip, port = str(address[0]), str(address[1])
        connectionarr.append(connection)
        print("[CONSOLE] - Connected with " + ip + ":" + port)
        threading.Thread(target=newClientThread, args=(connection, ip, port)).start()
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)