import socket
import sys

s = socket.socket()
print("Socket Created") ##creating a socket 
port = int(sys.argv[1])

s.connect(('127.0.0.1', port))  ##connecting to local host with specified port number
while True:
    send = input()
    s.sendall(send.encode())    ##sending the data to local dns server
    print("IP requested to Server for",send)
    msg=s.recv(1024)
    print("Ip obtained from server",msg.decode("utf-8"))
    exit()