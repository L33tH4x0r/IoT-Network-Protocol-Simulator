import threading
import time
import select
import socket

class ClientThread(threading.Thread):
    def __init__(self, client_ip, client_port, client):
        super(ClientThread, self).__init__()
        self.client = client
        self._stop = threading.Event()
        self.client_ip = client_ip
        self.client_port = client_port
        self.last_activity = time.time()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((client_ip, client_port))

    def run(self):
        # Start thread to handle recieving data        
        print "Client Thread Created\n"
        while not self.stopped():
            ready = select.select([self.client_socket], [], [], 2)
            if ready[0]:
                data, addr = self.client_socket.recvfrom(1024)
                self.last_activity = time.time()
                print "Recieved " + data + " from " + addr[0]
                # Open Socket with connection
                msg = "ACK " + self.client.userID
                print "Sending " + msg + " to " + addr[0]
                self.client_socket.sendto(msg, addr)

        print "Client Thread is Closing"

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
