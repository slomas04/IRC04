import socket
import threading
import os

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

