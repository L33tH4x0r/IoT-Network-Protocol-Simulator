import threading
import time
import select
import dropbox
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

class ServerThread(threading.Thread):
    def __init__(self, server, conn, addr):
        super(ServerThread, self).__init__()
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

        public_key = server.publickey.exportKey()
        print "Sending ", self.addr, " public key"
        self.server.server_socket.send(conn, public_key)
        fail_count = 0
        message = None
        while fail_count < 3:
            print "Waiting for client reply:"
            ready = select.select([self.server.server_socket.ssock], [], [], 10)
            if ready[0] :
                message = self.server.server_socket.rec(self.server.server_socket)
                print "recieved key from client"
                break
            else:
                fail_count += 1


        # Get public key from client
        if message:
            client_public_key = RSA.importKey(message)
            print self.client_public_key.exportKey()

        while not self.stopped():
            try:
                data = self.server.server_socket.rec(conn)
                print "Recieved: ", data
                self.last_activity = time.time()
                self.conn.settimeout(120)
                # Input data into server
                sent = self.server.input_data(data, conn, addr)
                # check if send was successful
                if sent == 0:
                    raise RuntimeError("ERROR: Message not sent")
                elif sent == "Ended Connection":
                    self.stop()
            except Exception,e:
                if e == 'timed out':
                    print self.addr, " Socket Timeout"
                    self.stop()

        print addr, " is exiting"

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
