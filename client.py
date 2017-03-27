################################################################################
# IMPORT LIBRARIES                  ############################################
################################################################################
import socket
import sys
import os
import time
import select
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
    fail_count = 0
    while fail_count < 3:
        print "Waiting for server reply:"
        ready = select.select([server_conn.ssock], [], [], 2)
        if ready[0] :
            client.recieve_msg(server_conn.rec(server_conn))
            return True
        else:
            fail_count += 1
    print "Packet dropped, message not recieved"
    return False

################################################################################
# MAIN PROGRAM                      ############################################
################################################################################

# Get user parameters
user_ID = sys.argv[1]
current_ip = sys.argv[2]
server_IP = sys.argv[3]
server_port = sys.argv[4]
# Create client
client = Client(user_ID, server_IP, server_port, current_ip )

while True:
    # Output Menu
    print "Options to talk with server"
    print "<R>egister with server"
    print "<D>eregister with device"
    print "<S>end Query to Device"
    print "Send <M>essage to Device"
    print "<V>iew All Saved Queries"
    print "<T>raceroute to Device"
    print "<P>ing to Device"
    print "<Q>uit"
    # Get Input from user
    command = raw_input("-> ").upper()
    print "\nProcessing Command: "
    # Process Command
    if command == 'R':
        # Register device with server
        print "Sending Register Command:\n"
        check_sent(client.register(), client.client_socket)

    elif command == 'D':
        # Deregister with server
        print "Sending Deregister command:\n"
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
            print ""
        # send query to server
        print "Sending Query Command\n"
        check_sent(client.query(str(command), to_id), client.client_socket)

    elif command == 'M':
        # Prompt user for device id to message
        print "Enter in the device ID you want to talk to:"
        to_id = raw_input("-> ")
        # Prompt user for message
        print "Enter in the message you want to send"
        message = raw_input("-> ")
        # Send message to server
        print "Sending Message Command"
        check_sent(client.message(to_id, message), client.client_socket)

    # elif command == 'V':
    #     if client.

    elif command == 'Q':
        # Prompt user
        print "Exiting connection:"
        # Tell server that you are getting off for now
        client.quit()
        # close socket
        client.client_socket.close()
        # exit program
        sys.exit(0)
