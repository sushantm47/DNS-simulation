import socket
import json
import sys


def dns(input):
    flag=0
    ##data stored locally
    file1 = open("data.txt","r")
    localdata = json.loads(file1.read())
    file1.close()
    ##checking if the requested site's ip exists locally
    for key,val in localdata.items():
        if(input==key):
            addr=val
            flag=1
    ##if data not found locally geting the ip from dns server
    if(flag==0):        
        addr = socket.gethostbyname(input)
        localdata[input] = addr            ##adding data to local data
    file1 = open("data.txt","w")
    file1.write(json.dumps(localdata))
    file1.close()
    return(addr)

s = socket.socket()
port = int(sys.argv[1])
print("Socket created")
s.bind(('',port))
print("socket binded to port",port)
s.listen(5)
print("Socket is listening")

while True:
    c,addr = s.accept()
    print("Connection received")
    data = c.recv(1024).decode()
    print(data)
    result=str(dns(data))
    print(result)
    c.send(bytes("".join(result),"utf-8"))
    c.close()
    exit()