import socket
import time
import threading
import os

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
