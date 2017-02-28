from datetime import datetime
class TrackedClients:
    def __init__(self, device_id, mac_address, client_ip, client_port):
        self.device_id = device_id
        self.mac_address = mac_address
        self.client_ip = client_ip
        self.client_port = client_port
        self.register_time = datetime.now()
        self.messages = []

    def get_time_in_str(self):
        return self.register_time.strftime('%Y-%m-%d %H:%M:%S')
