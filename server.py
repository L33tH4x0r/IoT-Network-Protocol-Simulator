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
server = Server(server_port_number, "127.0.0.1")
# Run server
while True:
    # Accept a connection
    conn, addr = server.server_socket.accept()
    print "Reciving connection from ", addr
    # Recieve data from connection
    data = conn.recv(server.server_socket.MAX_BUFFER_LEN)
    print "Recieved: ", data
    # Input data into server
    server.input_data(data, conn)
