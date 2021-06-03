import socket

UDP_IP = "192.168.11.193"
UDP_PORT = 4210
UDP_PORT2 = 4211

UDP_HOSTPORT = 1337
ADDR = (UDP_IP, UDP_PORT)
ADDR2 = (UDP_IP,UDP_PORT2)
HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)

def control(msg, address):
    sock.sendto(msg, address)
    
    try:
        data,addr = sock.recvfrom(1024)
    except:
        data = -1
        addr = -1

    print(data)
    print(addr)

    data = -1
    addr = -1

while True:
    message = input("command: ").encode()
    control(message, ADDR)

    message = input("command2: ").encode()
    control(message, ADDR2)