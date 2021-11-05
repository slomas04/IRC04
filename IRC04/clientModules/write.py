import socket
import threading
import os

def writetost(logtext): #writes to the scrolling stack box
    text_area.configure(state ='normal') #for this to work, the text area is temporarily enabled
    text_area.insert('end', "\n" + logtext) #text is inserted
    text_area.configure(state ='disabled')
    text_area.see("end")#then the text editing is disabled. This doesn't work perfectly but it'll do for now.

