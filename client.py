import socket
import sys

user_ID = sys.argv[1]
server_IP = sys.argv[2]
server_port = sys.argv[3]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.bind((socket.gethostname(),0))

print "Great Success!!"
