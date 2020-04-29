import socket
import json
import sys
import csv
from progressbar import ProgressBar
pbar = ProgressBar()


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
    newdata = {} 
    l=[]
    with open('top500Domains.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            name="".join(row[1])
            l.append(name)
        # print(newdata)
    error=0
    for remote_host in pbar(l):
            remote_host = remote_host.strip() # \n (new line) at the end of the line would cause error even when host exists
            try:
                addr=socket.gethostbyname(remote_host)
                # print(f"And IP address is ",addr)
                newdata[remote_host] = addr
            except socket.gaierror as se:
                error+=1
    print("Server successfully refreshed")
    file2 = open("data.json","w")
    file2.write(json.dumps(newdata))

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