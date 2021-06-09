import socket
import struct

class UDPsender:
    def __init__(self, UDP_IP="", UDP_PORT=0):
        self.UDP_IP = UDP_IP 
        self.UDP_PORT = UDP_PORT

    def send(self,command=b""):
        sock = socket.socket(socket.AF_INET, # Internet
               socket.SOCK_DGRAM) # UDP
        sock.sendto(command, (self.UDP_IP, self.UDP_PORT))

class UDPreceiver:
       def __init__(self, MCAST_GRP="", MCAST_PORT=0):
        self.MCAST_GRP = MCAST_GRP
        self.MCAST_PORT = MCAST_PORT

       def receive(self):

            IS_ALL_GROUPS = True

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if IS_ALL_GROUPS:
                # on this port, receives ALL multicast groups
                sock.bind(('', self.MCAST_PORT))
            else:
                # on this port, listen ONLY to MCAST_GRP
                sock.bind((self.MCAST_GRP, self.MCAST_PORT))
            mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)

            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            while True:
              print(sock.recv(10240))

