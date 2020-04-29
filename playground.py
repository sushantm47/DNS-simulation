import csv
import socket
import json

file1 = open("data.json","r")
localdata = json.loads(file1.read()) 

file1.close

l=[]
with open('top500Domains.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        name="".join(row[1])
        l.append(name)
    print(localdata)

for remote_host in l:
            remote_host = remote_host.strip() # \n (new line) at the end of the line would cause error even when host exists
            print(remote_host) 
            try:
                addr=socket.gethostbyname(remote_host)
                print(f"And IP address is ",addr)
                localdata[remote_host] = addr
            except socket.gaierror as se:
                print(f"Not done: {se}") # this will catch error when socket.gethostbyname

file1 = open("data.json","w")
file1.write(json.dumps(localdata))