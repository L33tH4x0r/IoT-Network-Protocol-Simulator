################################################################################
# IMPORT LIBRARIES                  ############################################
################################################################################
import socket
import sys
import os
import time
################################################################################
# IMPORT CUSTOM CODE                ############################################
################################################################################
execfile( os.getcwd() + "/StreamSocket.py" )
execfile( os.getcwd() + "/ClientClass.py" )
################################################################################
# FUNCTION DEFINITIONS              ############################################
################################################################################
def check_sent(sent, server_conn):
    if sent == 0:
        raise RunTimeError("Socket Connection Broken")
    # Get reply from client
    print "Waiting for server reply:"
    client.recieve_msg(client.client_socket.rec(server_conn))

################################################################################
# MAIN PROGRAM                      ############################################
################################################################################


# Get user parameters
user_ID = sys.argv[1]
server_IP = sys.argv[2]
server_port = sys.argv[3]
# Create client
client = Client(user_ID, server_IP, server_port)

while True:
    # Output Menu
    print "Options to talk with server"
    print "<R>egister with server"
    print "<D>eregister with device"
    print "<S>end Query to Device"
    print "Send <M>essage to Devive"
    print "<Q>uit"
    # Get Input from user
    command = raw_input("-> ").upper()
    # Process Command
    if command == 'R':
        # Register device with server
        check_sent(client.register(), client.client_socket)

    elif command == 'D':
        # Deregister with server
        check_sent(client.deregister(), client.client_socket)

    elif command == 'S':
        # Prompt user for query command
        print "Enter:"
        print "(1) To get IP and Port number of a device"
        print "(2) To check mailbox"
        command = int(raw_input("-> "))
        to_id = ""
        if command == 1:
            # Query user for device id
            print "Enter the device id you want to connect to"
            to_id = raw_input("-> ")
        # send query to server
        check_sent(client.query(command, to_id), client.client_socket)

    elif command == 'M':
        # Prompt user for device id to message
        print "Enter in the device ID you want to talk to:"
        to_id = raw_input("-> ")
        # Prompt user for message
        print "Enter in the message you want to send"
        message = raw_input("-> ")
        # Send message to server
        check_sent(client.message(to_id, message), client.client_socket)

    elif command == 'Q':
        # Prompt user
        print "Exiting connection:"
        # Tell server that you are getting off for now
        client.quit()
        # recieve ACK from server
        reply = client.recieve_msg(client.client_socket.rec(client.client_socket))
        # close socket
        client.client_socket.close()
        # exit program
        sys.exit(0)
