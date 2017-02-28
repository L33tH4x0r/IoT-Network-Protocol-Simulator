from uuid import getnode as get_mac
import socket
execfile( os.getcwd() + "/StreamSocket.py" )
class Client:
    def __init__(self, userID = "default_name", serverIP = "127.0.0.1", serverPort = "50000", mac = None, new_socket = None):
        # Add socket to client
        if new_socket:
            self.client_socket = new_socket
        else:
            self.client_socket = StreamSocket()
        # Give client identity
        self.userID = userID
        self.clientIP = socket.gethostname()
        # Bind socket to current hostname
        self.client_socket.bind((socket.gethostname(),0))
        self.clientPort = self.client_socket.ssock.getsockname()[1]
        # Connect client to server
        self.client_socket.connect((server_IP, int(server_port)))

        if mac:
            self.mac = mac
        else:
            self.mac = get_mac()

    def register(self):
        return "REGISTER ", self.userID, " ", self.mac, " ", self.clientIP, " ", self.clientPort

    def deregister(self):
        return "DEREGISTER ", self.userID, " ", self.mac

    def query(self, code = 1, to_id = ""):
        if code == 1:
            return "QUERY ", code, " ", self.userID, " ", to_id
        elif code == 2:
            return "QUERY ", code, " ", self.userID
