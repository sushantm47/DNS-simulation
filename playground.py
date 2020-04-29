import csv
import socket
import json

file2 = open("data.json","r")
newdata = json.loads(file2.read()) 

file2.close

l=[]
with open('top500Domains.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        name="".join(row[1])
        l.append(name)
    print(newdata)

for remote_host in l:
            remote_host = remote_host.strip() # \n (new line) at the end of the line would cause error even when host exists
            print(remote_host) 
            try:
                addr=socket.gethostbyname(remote_host)
                print(f"And IP address is ",addr)
                newdata[remote_host] = addr
            except socket.gaierror as se:
                print(f"Not done: {se}") # this will catch error when socket.gethostbyname

file2 = open("data.json","w")
file2.write(json.dumps(newdata))


# newdata = {} 
#     l=[]
#     with open('top500Domains.csv', 'r') as csv_file:
#         reader = csv.reader(csv_file)
#         for row in reader:
#             name="".join(row[1])
#             l.append(name)
#         # print(newdata)
#     error=0
#     for remote_host in pbar(l):
#             remote_host = remote_host.strip() # \n (new line) at the end of the line would cause error even when host exists
#             try:
#                 addr=socket.gethostbyname(remote_host)
#                 # print(f"And IP address is ",addr)
#                 newdata[remote_host] = addr
#             except socket.gaierror as se:
#                 error+=1
#     print(newdata)
#     print("Server successfully refreshed")
#     file2 = open("data.json","w")
#     file2.write(json.dumps(newdata))