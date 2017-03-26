# Import libraries
import socket
import sys
import os
# Get custom classes
execfile( os.getcwd() + "/StreamSocket.py"  )
execfile( os.getcwd() + "/ServerClass.py"   )
execfile( os.getcwd() + "/ClientThread.py"  )
execfile( os.getcwd() + "/ThreadManager.py" )
# Get input from user
server_port_number = sys.argv[1]
# Create server socket.gethostname() with raspberry pi
server = Server(server_port_number, "127.0.0.1")
# Start thread manager
thread_manager = ThreadManager(server)
thread_manager.start()

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
        new_thread = ClientThread(server, conn, addr)
        # Start Thread
        print "Starting Thread"
        new_thread.start()
        # Track new thread
        thread_manager.add_thread(new_thread)
    except Exception,e:
        print e
        print "Socket timeout on new connection"
