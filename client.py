import socket
import sys
import os

execfile( os.getcwd() + "/StreamSocket.py" )
execfile( os.getcwd() + "/ClientClass.py" )
# Get user parameters
user_ID = sys.argv[1]
server_IP = sys.argv[2]
server_port = sys.argv[3]
# Create client
client = Client(user_ID, server_IP, server_port)
# Create test case
sent = client.register()
# Check if connection exists
if sent == 0:
    raise RunTimeError("Socket Connection Broken")
# recieve data from server
data = client.client_socket.ssock.recv(1024)
# print recieved data
print "recieved", data
# close socket
client.client_socket.close()
