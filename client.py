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
    print "Send <M>essage to Device"
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

    elif command == 'M':
        check_sent(client.message(to_id, message), client.client_socket)

    elif command == 'Q':
        # Prompt user
        print "Exiting connection:"
        # Tell server that you are getting off for now
        client.quit()
        # close socket
        client.client_socket.close()
        # exit program
        sys.exit(0)
