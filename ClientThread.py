import threading
import time
import socket.timeout as TimeoutException

class ClientThread(threading.Thread):
    def __init__(self, server, conn, addr):
        super(ClientThread, self).__init__()
        self._stop = threading.Event()
        self.server = server
        self.conn = conn
        self.addr = addr
        self.last_activity = time.time()
        self.server.server_socket.settimeout(5)

    def run(self):
        # Start thread to handle recieving data
        print "Thread Created"
        print "Recieving Data from ", self.addr
        self.last_activity = time.time()
        data = self.server.server_socket.rec(conn)
        print "Recieved: ", data
        self.last_activity = time.time()
        # Input data into server
        sent = self.server.input_data(data, conn, addr)
        # check if send was successful
        if sent == 0:
            raise RuntimeError("ERROR: Message not sent")
        # Loop for communication if client wants to talk still
        while sent != "Ended Connection" or not self.stopped():
            # Recieve data from connection
            data = self.server.server_socket.rec(self.conn)
            print "Recieved: ", data
            # Input data into server
            sent = self.server.input_data(data, self.conn, self.addr)
            # check if send was successful
            if sent == 0:
                raise RuntimeError("ERROR: Message not sent")

        print addr, " is exiting"

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()