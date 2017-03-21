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
            # Run register message handling
            return self.register_device(conn, parsed_data[1], parsed_data[2], parsed_data[3], parsed_data[4])
        # elif command == "QUIT":
        #     # Run Quit handler
        #     return self.quit(parsed_data[1])

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
        self.clients.append(TrackedClients(device_id, mac_address, client_ip, client_port))
        # send ack for register
        return self.new_device_ack(conn, device_id)
    #
    # def quit(self, device_id):
    #     # Search through clients for the device id
    #     for client in self.clients:
    #         if client.device_id == device_id:


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
