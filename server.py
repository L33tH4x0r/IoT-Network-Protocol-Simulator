import socket
import sys
import os

execfile( os.getcwd() + "/StreamSocket.py" )

server_port_number = sys.argv[1]
server_ip_number = sys.argv[2]

server_socket = StreamSocket()

server_socket.bind((server_ip_number, int(server_port_number)))

server_socket.listen()
while True:
    conn, addr = server_socket.accept()
    print "Reciving connection from ", addr
    data = conn.recv(1024)
    print "Recieved", data

    conn.send(data.upper())
