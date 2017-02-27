import socket
import sys
import os

execfile( os.getcwd() + "/StreamSocket.py" )

server_port_number = sys.argv[1]
server_ip_number = sys.argv[2]

server_socket = StreamSocket()

server_socket.bind((server_ip_number, int(server_port_number)))

while True:
    data, addr = server_socket.rec()
    
    server_port_number.send(data.upper())
