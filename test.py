# first of all import the socket library
import socket            
 
# next create a socket object
s = socket.socket()        
s.connect(("127.0.0.1", 6969))
s.send("blacklist".encode())
