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

    def listen (self):
        self.ssock.listen(self.MAX_SOCKET_NUMBER)

    def accept(self):
        return self.ssock.accept()

    def close(self):
        self.ssock.close()

    def settimeout(self, duration):
        self.ssock.settimeout(duration)

    def recv(self, buffer_size):
        return self.ssock.recv(buffer_size)

    def send(self, conn, msg):
        # Initialize sent counter
        totalsent = 0
        msg = msg + "@"
        # Loop through message
        while totalsent < len(msg):
            try:
                # Send max stream size amount of bytes starting from the most recent byte sent
                sent = conn.send(msg[totalsent:totalsent+self.MAX_BUFFER_LEN])

                # check if socket connection loss
                if sent == 0:
                    print "Connection lost"

                # update the total sent
                totalsent = totalsent + sent
            except Exception, e:
                print "Waiting for client: "

    def rec(self, conn):
        # initialize msg buffer
        msg = []
        data = ""
        # Cycle through recieving stream
        while True:
            # Recieve data from socket
            data = conn.recv(self.MAX_BUFFER_LEN)

            if data != "":
                # add recieved data from socket
                if data[-1] == "@":
                    # Add data minus terminating character
                    msg.append(data[0:-1])
                    #return data received in one string
                    return ''.join(msg)
                else:
                    msg.append(data)
