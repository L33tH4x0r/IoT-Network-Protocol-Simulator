import socket
import sys
import os

execfile( os.getcwd() + "/StreamSocket.py" )

user_ID = sys.argv[1]
server_IP = sys.argv[2]
server_port = sys.argv[3]

client_socket = StreamSocket()

# client_socket.bind((socket.gethostname(),0))

client_socket.connect((server_IP, int(server_port)))

sent = client_socket.ssock.sendall("TesTStRinG")

if sent == 0:
    raise RunTimeError("Socket Connection Broken")

data = client_socket.ssock.recv(1024)

print "recieved", data
client_socket.ssock.close()
