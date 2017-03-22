from uuid import getnode as get_mac
import socket
execfile( os.getcwd() + "/StreamSocket.py" )
class Client:
    # CLASS CONSTANTS ##########################################################
    ############################################################################
    NO_MSG_CNT_ERROR = "ERROR: Malformed packet, valid number not in message count place\n"
    ID_TAKEN_ERROR = "ERROR: device ID already taken, please use another\n"
    SERVER_ID_ERROR = "ERROR: wrong ID returned, should have gotten NACK\n"

    # CLASS MANAGERS ###########################################################
    ############################################################################
    def __init__(   self,
                    userID,
                    serverIP,
                    serverPort,
                ):
        # Add socket to client
        self.client_socket = StreamSocket()
        # Bind socket to current hostname
        self.client_socket.bind((socket.gethostname(),0))
        # Give client identity
        self.userID = userID
        self.clientIP = self.client_socket.ssock.getsockname()[0]
        self.clientPort = self.client_socket.ssock.getsockname()[1]
        # Connect client to server
        self.client_socket.connect((server_IP, int(server_port)))
        # Add MAC address of current machine
        self.mac = get_mac()
        # create error log
        self.error_log = open('error.log', 'a')
        self.error_log.close()

    # PROTOCOL MESSAGES ########################################################
    ############################################################################
    def register(self):
        # send message
        return self.send("REGISTER " + self.userID + " " + str(self.mac) + " " +
            str(self.clientIP) + " " + str(self.clientPort))

    def deregister(self):
        # Send message
        return self.send("DEREGISTER " + self.userID + " " + self.mac)

    def query(self, code, to_id):
        # Check code
        if code == "1":
            return self.send("QUERY " + code + " " + self.userID + " " + to_id)
        elif code == "2":
            return self.send("QUERY " + code + " " + self.userID)

    def quit(self):
        # Send Mesage
        return self.send("QUIT " + self.userID)

    def deregister(self):
        # Send message
        return self.send("DEREGISTER " + self.userID + " " + str(self.mac))

    def message(self, to_id, send_message):
        return self.send("MSG " + self.userID + " " + to_id + " " + send_message)


    # COMMUNICATION ############################################################
    ############################################################################
    def send(self, msg):
        print "Sending: ", msg
        return self.client_socket.send(self.client_socket.ssock, msg)

    def recieve_msg(self, msg):
        # Check if conneciton broken
        if msg == "":
            print "Connection lost"
            return None
        # print message recieved
        print "Recieved: ", msg, "\n"
        # parse msg
        parsed_msg = msg.split()
        # check if ACK
        if parsed_msg[0] == "ACK":
            return self.receive_ack(parsed_msg)
        # check if NACK
        elif parsed_msg[0] == "NACK":
            if parsed_msg[2] == self.userID:
                print "\nID registered to different mac: ", parsed_msg[3]
                return None
            else:
                print "\nDuplicate registration, can only have one id for device: "
                print "Device registered under: ", parsed_msg[2]
                return None

    def receive_ack(self, msg):
        # Check status code
        if msg[1] == '1':
            # Check if the returned user id is correct
            if msg[2] == self.userID:
                return self.check_messages(msg)
            # Device id already taken, error on server end
            else:
                raise RuntimeError(self.SERVER_ID_ERROR)
                self.write_to_log(self.SERVER_ID_ERROR)
                return None


    def check_messages(self, msg):
        # Check if already registered
        if len(msg) > 3:
            # check if new messages
            try:
                if int(msg[3]) > 0:
                    print "\nAlready registered, server has ", int(msg[3]), " new messages\n"
                    return self.getNewMessages()
                else:
                    print "\nAlready registered, no new messages\n"
                    return None
            except Exception, e:
                print e
                self.write_to_log(self.NO_MSG_CNT_ERROR)
                return None
        # Device was newly registered
        else:
            print "\nSuccessfully registered with server\n"
            return None



    # ERROR HANDLING ###########################################################
    ############################################################################
    def write_to_log(self, msg):
        self.error_log = open('error.log', 'a')
        self.error_log.write(msg)
        self.error_log.close
