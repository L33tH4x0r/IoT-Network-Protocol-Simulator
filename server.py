# Import libraries
import socket
import sys
import os
# Get custom classes
execfile( os.getcwd() + "/StreamSocket.py"  )
execfile( os.getcwd() + "/ServerClass.py"   )
execfile( os.getcwd() + "/ServerThread.py"  )
execfile( os.getcwd() + "/ThreadManager.py" )
# Get input from user
server_ip_address = sys.argv[1]
server_port_number = sys.argv[2]
# Create server socket.gethostname() with raspberry pi
server = Server(server_port_number, server_ip_address )
# Start thread manager
# thread_manager = ThreadManager(server)
# thread_manager.start()

# Run server
while True:
    # Accept a connection
    print "Waiting to recieve connection\n"
    try:
        conn, addr = server.server_socket.accept()
        conn.settimeout(5)
        print "Reciving connection from ", addr
        # Create thread
        print "Creating Thread:"
        new_thread = ServerThread(server, conn, addr)
        # Start Thread
        print "Starting Thread"
        new_thread.start()
        # Track new thread
        # thread_manager.add_thread(new_thread)
    except Exception,e:
        print e
        print "Socket timeout on new connection"
