from uuid import getnode as get_mac
import socket
execfile( os.getcwd() + "/StreamSocket.py" )
execfile(os.getcwd() + "/TrackedClients.py")
class Server:
    def __init__ (self, server_port = "50000", server_IP = "127.0.0.1", new_socket = None):
        # Check for new socket
        if new_socket:
            self.server_socket = new_socket
        else:
            self.server_socket = StreamSocket()
        # Create socket for server
        self.server_socket.bind((server_IP, int(server_port)))
        # Start listening
        self.server_socket.listen()
        # Create clients list
        self.clients = []

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
                if client.device_id == parsed_data [1]:
                    # check if it belongs to the device calling it
                    if client.mac_address == parsed_data[2]:
                        # Send a success
                        return self.ack(conn, client.device_id, len(client.messages), client.get_time_in_str())
                    else:
                        # Send a failure
                        return 0
            # Device id not found:
            #
            # Append new client to clients list with their:
            #
            #                                  device id,    mac address,     ip address,    port number
            self.clients.append(TrackedClients(parsed_data[1], parsed_data[2], parsed_data[3], parsed_data[4]))
            # send ack for register
            return self.ack(conn, parsed_data[1])

    def ack(self,conn, device_id, count = None, time = None):
        if count:
            message = "ACK 1 " + device_id + " " + str(count) + " " + time
            print "Sent: ", message
            return conn.send(message)
        else:
            message = "ACK 1 " + device_id
            print "Sent: ", message
            return conn.send("ACK 1 " + device_id)
