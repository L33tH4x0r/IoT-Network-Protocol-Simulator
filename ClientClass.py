from uuid import getnode as get_mac
import socket
import os
import subprocess
import dropbox
import datetime
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

execfile( os.getcwd() + "/StreamSocket.py" )
execfile( os.getcwd() + "/ClientThread.py" )
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
                    currentIP
                ):
        # Add socket to client
        self.client_socket = StreamSocket()
        # Bind socket to current hostname
        self.client_socket.bind((currentIP,0))
        # Give client identity
        self.userID = userID
        self.clientIP = self.client_socket.ssock.getsockname()[0]
        self.clientPort = self.client_socket.ssock.getsockname()[1]
        # Connect client to server
        self.client_socket.connect((server_IP, int(server_port)))

        fail_count = 0
        message = None
        while fail_count < 3:
            print "Waiting for server reply:"
            ready = select.select([self.client_socket.ssock], [], [], 2)
            if ready[0] :
                message = self.client_socket.rec(self.client_socket)
                print "recieved key from server"
                break
            else:
                fail_count += 1

        # Get public key from server
        self.public_key = 16
        if message:
            self.server_public_key = RSA.importKey(message)
            print self.server_public_key.exportKey()
            # Create keys for client
            self.key = RSA.generate(1024) #generate pub and priv key
            self.publickey = self.key.publickey() # pub key export for exchange
            public_key = self.publickey.exportKey()
            print "Sending server public key"
            self.client_socket.send(self.client_socket, public_key)
        else:
            print "server not responding"

        # Add MAC address of current machine
        self.mac = get_mac()
        # create error log
        self.error_log = open('error.log', 'a')
        self.error_log.close()
        self.queried_devices = []
        # Open UDP socket
        self.client_thread = ClientThread(self.clientIP, self.clientPort, self)
        self.client_thread.start()
        self.dbx = dropbox.Dropbox('AaOxbynKDoAAAAAAAAAAfWGBFWKm5iRoD6nNXqnuKs_sfKxBPTLe3hTX_G_GVCE0')

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
        # Close UDP thread
        self.client_thread.stop()
        # Send Mesage
        return self.send("QUIT " + self.userID)

    def deregister(self):
        # Send message
        return self.send("DEREGISTER " + self.userID + " " + str(self.mac))

    def message(self, send_message):
        return self.send(send_message)


    # COMMUNICATION ############################################################
    ############################################################################
    def send(self, msg):
        print "Sending: ", msg
        return self.client_socket.send(self.client_socket.ssock, self.server_public_key.encrypt(msg, self.key)[0])

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
        if msg[1] == '2':
            # parse message
            device_id       = msg[4]
            device_ip       = msg[2]
            device_port     = int(msg[3])
            # Check if device already exists
            for device in self.queried_devices:
                if device[0] == device_id:
                    device[1] = device_ip
                    device[2] = device_port
                    return None
            # Add device to tracked queries
            self.queried_devices.append([device_id, device_ip, device_port])
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

    # UDP Messages #############################################################
    ############################################################################
    def traceroute(self, device_name):
        # for device in self.queried_devices:
        #     if device[0] == device_name:
        #         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #         trace_message = "traceroute " + device[1]
        #         trace = subprocess.check_output(os.system(trace_message))
        #         msg = "DATA " + str(self.userID) + " trace " + " " + str(trace)
        #         count = 0
        #         while count < 3:
        #             sock.sendto(msg, (device[1], device[2]))
        #             count += 1
        #         return True

        print "Device not found, please query to maske sure alive"
        return False

    def ping(self, device_name):
        for device in self.queried_devices:
            if device[0] == device_name:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                msg = "DATA " + str(self.userID) + " ping"
                file_name = "/" + self.userID + ".txt"
                count = 0
                self.dbx.files_download_to_file(os.getcwd() +file_name, file_name)
                f = open(file_name[1:len(file_name)], 'a+')
                sock.sendto(msg, (device[1], device[2]))
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(time_now + " " + msg + "\n")
                while count < 2:
                    sock.sendto(msg, (device[1], device[2]))
                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(time_now + " " + msg + "\n")
                    count += 1
                # Delete file at dropbox
                print "Deleting file at Dropbox"
                print self.dbx.files_delete(file_name)
                # Upload changes to file to DropBox
                print "Sending file to Dropbox"
                f.seek(0)
                print f.read()
                f.seek(0)
                print self.dbx.files_upload(f.read(), file_name)
                # Push notification to server
                msg = "UPDATED " + self.userID
                print "Sent ", self.send(msg), " to server"
                # Delete local version of file
                print "Removing local file from DropBox"
                os.remove(os.getcwd() + file_name)
                return True

        print "Device not found, please query to make sure alive"
        return False


    # ERROR HANDLING ###########################################################
    ############################################################################
    def write_to_log(self, msg):
        self.error_log = open('error.log', 'a')
        self.error_log.write(msg)
        self.error_log.close
