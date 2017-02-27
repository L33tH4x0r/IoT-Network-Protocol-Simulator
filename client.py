import socket
import sys

user_ID = sys.argv[1]
server_IP = sys.argv[2]
server_port = sys.argv[3]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.bind((socket.gethostname(),0))

server = (server_IP, server_port)

client_socket.sendto("TesTStRinG", server)

data, addr = client_socket.recfrom(1024)
print "recieved", data, "from", addr
client_socket.close()
