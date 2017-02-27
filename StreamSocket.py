import socket
import sys

class StreamSocket:
    # Constants
    MAX_BUFFER_LEN = 1024
    MAX_SOCKET_NUMBER = 3

    def __init__(self, NewSocket = None):
        if NewSocket == None:
            self.ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.ssock = NewSocket
    def bind(self, address):
        self.ssock.bind(address)

    def connect(self, addr):
        # initialize connection with input
        self.ssock.connect(addr)

    def send(self, msg):
        # Initialize sent counter
        totalsent = 0
        # Loop through message
        while totalsent < len(msg):
            # Send max stream size amount of bytes starting from the most recent byte sent
            sent = self.ssock.send(msg[totalsent:totalsent+self.MAX_BUFFER_LEN])
            # check if socket connection loss
            if sent == 0:
                print "Connection lost"
                break
            # update the total sent
            totalsent = totalsent + sent
        # let other side know you are done
        self.ssock.send("\0")

    def rec(self):
        # initialize msg buffer
        msg = []
        data = ""
        # Start listening
        self.ssock.listen(self.MAX_SOCKET_NUMBER)
        # Cycle through recieving stream
        while data != "\0":
            # Accept data from socket
            conn, addr = self.ssock.accept()
            # print address received from
            print "Recieved data from ", addr
            # Recieve data from socket
            data = conn.recv(1024)
            # check for socket connection loss
            if data == "":
                print "Connection lost"
                break
            # add recieved data from socket
            msg.append(data)
        #return data received in one string
        return ''.join(msg), addr
