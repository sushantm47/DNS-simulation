import socket
import json
import sys
import csv
import alive_progress
from alive_progress import alive_bar
import time

def dns(input):
    flag=0
    ##data stored locally
    file1 = open("data.json","r")
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
    file1 = open("data.json","w")
    file1.write(json.dumps(localdata))
    file1.close()
    return(addr)

def startserver():
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

def refreshserverdata():
    localdata={}
    l=[]
    with open('top500Domains.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            name="".join(row[1])
            l.append(name)
    with alive_bar(len(l)) as bar:
        for remote_host in l:
            remote_host = remote_host.strip() # \n (new line) at the end of the line would cause error even when host exists
            # print(remote_host) 
            try:
                addr=socket.gethostbyname(remote_host)
                # print(f"And IP address is ",addr)
                localdata[remote_host] = addr
            except socket.gaierror as se:
                i=0
                # print(f"Not done: {se}") # this will catch error when socket.gethostbyname
            bar()
            time.sleep(0.1)
    file1 = open("data.json","w")
    file1.write(json.dumps(localdata))
    print("Successfully refreshed")

# refreshserverdata()
flag=1
print("DNS SERVER"," 1  -> Start server"," 2  -> Refresh server data","-1  -> Quit",sep="\n")
while flag:
    t=int(input())
    if(t==1):
        startserver()
    elif(t==2):
        refreshserverdata()
    elif(t==-1):
        print("Shutting down the server..","Successfully shutdown",sep="\n")
        flag=0
    else:
        print("please enter valid choice")