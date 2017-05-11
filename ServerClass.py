from uuid import getnode as get_mac
from datetime import datetime
import socket
import threading
import time
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
execfile( os.getcwd() + "/StreamSocket.py" )
execfile(os.getcwd() + "/TrackedClients.py")

class Server:
    # CLASS MANAGERS ###########################################################
    ############################################################################
    def __init__ (  self,
                    server_port,
                    server_IP,
                    ):
        # Check for new socket
        self.server_socket = StreamSocket()
        # Create socket for server
        self.server_socket.bind((server_IP, int(server_port)))
        # Start listening
        self.server_socket.listen()
        # Create clients list
        self.clients = []
        # Open error log
        self.error_log = open('error.log', 'a')
        self.dbx = dropbox.Dropbox('AaOxbynKDoAAAAAAAAAAfWGBFWKm5iRoD6nNXqnuKs_sfKxBPTLe3hTX_G_GVCE0')

        self.key = RSA.generate(1024) #generate pub and priv key
        self.publickey = self.key.publickey() # pub key export for exchange

    # COMMUNICATION ############################################################
    ############################################################################
    def input_data(self, data, conn, addr):
        # parse data
        parsed_data = data.split()
        # Get command
        command = parsed_data[0]
        # check if register command
        if command == "REGISTER":
            # Run register message handling
            return self.register_device(conn, parsed_data[1], parsed_data[2], parsed_data[3], parsed_data[4])
        elif command == "QUIT":
            # Run Quit handler
            return self.quit(parsed_data[1])
        elif command == "DEREGISTER":
            # Run Deregister handler
            return self.deregister(conn, parsed_data[1], parsed_data[2])
        elif command == "QUERY":
            # Run Query Handler
            if parsed_data[1] == "1":
                return self.query(conn, parsed_data[1], parsed_data[3] )
            else:
                return self.query(conn, parsed_data[1], parsed_data[2] )
        elif command == "MSG":
            # Run the message handler
            return self.message(conn, parsed_data[1], parsed_data[2], parsed_data[3])
        # elif command == "UPDATED":
        #     # Run the message handler
        #     # TODO :: Create a message that pings server when client updates to
        #     # Dropbox. Create action to pull data from server. Create object to
        #     # # store data from Dropbox.
        #     # return self.message(conn, parsed_data[1], parsed_data[2])

    def send(self, conn, msg):
        # Print the message thats being sent
        print "Sent: ", msg
        # send message
        return self.server_socket.send(conn, msg)

    # DATA MANAGEMENT ##########################################################
    ############################################################################
    def register_device(self, conn, device_id, mac_address, client_ip, client_port):
        # check for device already existing
        for client in self.clients:
            # check if device id exists
            if client.device_id == device_id:
                # check if it belongs to the device calling it
                if client.mac_address == mac_address:
                    # Add connection to client
                    client.connection = conn
                    # Update information from client
                    client.client_ip = client_ip
                    client.client_port = client_port
                    # Send a success
                    return self.ack_w_msg_count(conn, client.device_id, len(client.messages), client.get_time_in_str())
                # device id already registered to another mac address
                else:
                    # Send a failure
                    return self.dup_nack(conn, client.device_id, client.mac_address)
            # check if mac address already exists
            elif client.mac_address == mac_address:
                    # Send a failure
                    return self.dup_nack(conn, client.device_id, client.mac_address)
        # Device not found

        # Append new client to clients list
        self.clients.append(TrackedClients(device_id, mac_address, client_ip, client_port, conn))
        # Create file for device to upload to
        file_message = "DEVICE NAME: " + device_id + "\n\n"
        file_name = "/"+device_id+".txt"
        print "Uploading", file_name, " to dropbox"
        print "Response from server:"
        print self.dbx.files_upload(file_message, file_name)
        # send ack for register
        return self.new_device_ack(conn, device_id)

    def quit(self, device_id):
        # Search through clients for the device id
        for client in self.clients:
            if client.device_id == device_id:
                client.active = False
                client.connection = None
                print "Ended connection with device id: " + device_id
                return "Ended Connection"

        print "Device ID not found"
        return "Ended Connection"

    def deregister(self, conn, device_id, mac_address):
        # find device id
        for client in self.clients:
            if client.device_id == device_id:
                if client.mac_address == mac_address:
                    self.clients.remove(client)
                    print "Device ID " + device_id + " Successfully Removed"
                    return self.deregister_ack(conn, device_id)
                else:
                    print "ERROR: MAC Address Not registered to device id: " + device_id
                    return self.deregister_nack(conn, client.device_id, client.mac_address)
        else:
            print "Device Id " + device_id + " not found, returning ack"
            return self.deregister_ack(conn, device_id)

    def query(self, conn, code, device_id):
        if code == "1":
            for client in self.clients:
                if client.device_id == device_id:
                    print "Device ID " + device_id + " found, returning ip address and port number of client"
                    return self.query_client_ack(conn, client.client_ip, client.client_port, device_id)

            print "Device ID " + device_id + " not found, returning nack to client"
            return self.query_client_nack(conn)
        elif code == "2":
            for client in self.clients:
                if client.device_id == device_id:
                    print "Device ID " + device_id + " found, returning count of messages back"
                    return self.ack_w_msg_count(conn, client.device_id, len(client.messages), datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
            print "Device ID " + device_id + " not found, returning nack"
            return self.query_client_nack(conn)

    def message(self, conn, from_id, to_id, message):
        # Search for device
        for client in self.clients:
            if client.device_id == to_id:
                # hold message for when they login again
                client.messages.append([from_id, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                print "Device ID " + to_id  + " found. Saved message to be sent"
                # Send client an ack to mention we got it
                return self.message_recieved_ack(conn, to_id)
        # Client not found
        print "Device ID " + to_id + " not found, sending error to client"
        return self.message_nack(conn, to_id)


    # MESSAGES #################################################################
    ############################################################################
    def ack_w_msg_count(self, conn, device_id, count, time):
        msg = "ACK 1 " + device_id + " " + str(count) + " " + time
        return self.send(conn, msg)

    def new_device_ack(self, conn, device_id):
        msg = "ACK 1 " + device_id
        return self.send(conn, msg)

    def dup_nack(self, conn, device_id, mac_address):
        msg = "NACK 1 " + device_id + " " + mac_address
        return self.send(conn, msg)

    def query_client_nack(self, conn):
        msg = "NACK 2"
        return self.send(conn, msg)

    def deregister_nack(self, conn, device_id, mac):
        msg = "NACK 3 " + mac + " " + device_id
        return self.send(conn, msg)

    def deregister_ack(self, conn, device_id):
        msg = "ACK 3 " + device_id
        return self.send(conn, msg)

    def query_client_ack(self, conn, client_ip, client_port, device_id):
        msg = "ACK 2 " + client_ip + " " + client_port + " " + device_id
        return self.send(conn, msg)

    def send_message(self, conn, from_id, to_id, message, time):
        msg = "MSG " + from_id + " " + to_id + " " + message + " " + time
        return self.send(conn, msg)
    def message_recieved_ack(self, conn, to_id):
        msg = "ACK 5 " + to_id + " " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.send(conn, msg)

    def message_nack(self, conn, to_id):
        msg = "NACK 5 " + to_id
        return self.send(conn, msg)
