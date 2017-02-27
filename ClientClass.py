from uuid import getnode as get_mac

class Client:
    def __init__(self, userID = None, clientIP = None, clientPort = None, mac = None):
        self.userID = userID
        self.clientIP = clientIP
        self.clientPort = clientPort
        if mac:
            self.mac = mac
        else:
            self.mac = get_mac()

    def register(self):
        return "REGISTER ", self.userID, " ", self.mac, " ", self.clientIP, " ", self.clientPort

    def deregister(self):
        return "DEREGISTER ", self.userID, " ", self.mac

    def query(self, code = 1, to_id):
        if code == 1:
            return "QUERY ", code, " ", self.userID, " ", to_id
        elif code == 2:
            return "QUERY ", code, " ", self.userID
