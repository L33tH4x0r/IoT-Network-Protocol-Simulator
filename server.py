# Import libraries
import socket
import sys
import os
# Get custom classes
execfile( os.getcwd() + "/StreamSocket.py" )
execfile( os.getcwd() + "/ServerClass.py" )
# Get input from user
server_port_number = sys.argv[1]
# Create server socket.gethostname() with raspberry pi
server = Server(server_port_number)
# Run server
while True:
    # Accept a connection
    conn, addr = server.server_socket.accept()
    print "Reciving connection from ", addr
    # Recieve data from connection
    data = conn.recv(1024)
    print "Recieved", data
    # return received data as uppercase string
    conn.send(data.upper())
