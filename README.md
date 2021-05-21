# IRC04
IRC04 is a simple, Encrypted Chat Client/Server made in python 3. The client uses TKinter as a frontend and the server currently only uses the command line.
![kermit](https://i.imgur.com/5mzqChX.png)

## Prerequisites
* Python 3 (3.7.3 to be exact)
* Socket
* Tkinter
* Threading
* Time

(Note that most, if not all of these modules are installed by default)

## To-Do list
* ~~Let the client pick and IP and Port~~
* ~~Let the server pick IP and Port~~
* ~~Make a server Frontend in TKinter to properly process serverside commands~~
* ~~safely close the server~~
* ~~Add a form of encryption for privacy~~
* Give IP, Port and Username selection a proper frontend
* Add more Client and Server commands

## How to run

### Server
* Make sure that the port you want to host on has been forwarded if you're using this across networks
* run ```server.py```
* Enter your local IP address (NOT LOCALHOST OR 127.0.0.1)
* Enter the Server Port
* All Done!

### Client
* run ```client.py```
* Enter the server's IP address
* Enter the server's port
* Enter your desired username
* Done! you can now use the text box to type and you can use !04help for a list of commands
