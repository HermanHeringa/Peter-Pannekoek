import socket

class UDPsocket:
    def __init__(self, UDP_IP="", UDP_PORT=0):
        self.UDP_IP = UDP_IP 
        self.UDP_PORT = UDP_PORT

    def send(self,command=b""):
        sock = socket.socket(socket.AF_INET, # Internet
               socket.SOCK_DGRAM) # UDP
        sock.sendto(command, (self.UDP_IP, self.UDP_PORT))
