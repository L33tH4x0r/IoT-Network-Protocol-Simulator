import threading
import time
import select
import socket

class ClientThread(threading.Thread):
    def __init__(self, client_ip, client_port):
        super(ClientThread, self).__init__()
        self._stop = threading.Event()
        self.conn = conn
        self.addr = addr
        self.last_activity = time.time()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((client_ip, client_port))

    def run(self):
        # Start thread to handle recieving data
        print "Thread Created"
        while not self.stopped():
            data, addr = self.client_socket.recvfrom(1024)
            print "Recieved " + data + " from " + addr


        print self.addr, " is exiting"

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
