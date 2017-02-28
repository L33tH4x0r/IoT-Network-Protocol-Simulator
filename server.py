import socket
import sys
import os

execfile( os.getcwd() + "/StreamSocket.py" )

server_port_number = sys.argv[1]

server_socket = StreamSocket()

# socket.gethostname() with raspberry pi
server_socket.bind(("127.0.0.1", int(server_port_number)))

server_socket.listen()
while True:
    conn, addr = server_socket.accept()
    print "Reciving connection from ", addr
    data = conn.recv(1024)
    print "Recieved", data

    conn.send(data.upper())
