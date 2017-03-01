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
# Register device with server
sent = client.register()
# Check if connection exists
if sent == 0:
    raise RunTimeError("Socket Connection Broken")
# recieve ACK from server
recieved = client.recieve_msg(client.client_socket.ssock.recv(1024))
if not recieved:
    sys.exit(0)
# close socket
client.client_socket.close()
# exit program
sys.exit(0)
