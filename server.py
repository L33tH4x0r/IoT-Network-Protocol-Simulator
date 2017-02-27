import socket
import sys

server_port_number = sys.argv[1]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind((socket.gethostname(),int(server_port_number)))
