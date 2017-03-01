from uuid import getnode as get_mac
import socket
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

    # COMMUNICATION ############################################################
    ############################################################################
    def input_data(self, data, conn):
        # parse data
        parsed_data = data.split()
        # Get command
        command = parsed_data[0]
        # check if register command
        if command == "REGISTER":
            # check for device already existing
            for client in self.clients:
                # check if device id exists
                if client.device_id == parsed_data[1]:
                    # check if it belongs to the device calling it
                    if client.mac_address == parsed_data[2]:
                        # Send a success
                        return self.ack_w_msg_count(conn, client.device_id, len(client.messages), client.get_time_in_str())
                    # device id already registered to another mac address
                    else:
                        # Send a failure
                        return self.dup_nack(conn, client.device_id, client.mac_address)
                # check if mac address already exists
                elif client.mac_address == parsed_data[2]:
                    # Send a failure
                    return self.dup_nack(conn, client.device_id, client.mac_address)
            # Device not found
            #
            # Append new client to clients list with their:
            #
            #                                       device id,    mac address,     ip address,    port number
            self.clients.append(TrackedClients(parsed_data[1], parsed_data[2], parsed_data[3], parsed_data[4]))
            # send ack for register
            print parsed_data[2]
            return self.new_device_ack(conn, parsed_data[1])

    def send(self, conn, msg):
        print "Sent: ", msg
        return conn.send(msg)

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
