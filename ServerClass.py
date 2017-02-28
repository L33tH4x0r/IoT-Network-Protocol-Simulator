from uuid import getnode as get_mac
import socket
execfile( os.getcwd() + "/StreamSocket.py" )
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
