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
    # Prime loop
    # Recieve data from connection
    data = server.server_socket.rec(conn)
    print "Recieved: ", data
    # Input data into server
    sent = server.input_data(data, conn, addr)
    # check if send was successful
    if sent == 0:
        raise RuntimeError("ERROR: Message not sent")
    # Loop for communication if client wants to talk still
    while sent != "Ended Connection":
        # Recieve data from connection
        data = server.server_socket.rec(conn)
        print "Recieved: ", data
        # Input data into server
        sent = server.input_data(data, conn, addr)
        # check if send was successful
        if sent == 0:
            raise RuntimeError("ERROR: Message not sent")
