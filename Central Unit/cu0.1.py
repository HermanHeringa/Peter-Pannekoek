import socket
import threading
import time

UDP_IP = "192.168.11.193"
UDP_HOSTPORT = 1337

address_list = []

HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)
sock.settimeout(0)

def get_millis():
    return round(time.time() * 1000)

def send_msg(msg, address):
    print(f"[SENT]{msg},{address}")
    sock.sendto(msg.encode(), address)
    
def handle_bot(data, address):

    timeout_counter = 0
    start_time = get_millis()

    while True:
        
        

        #Every 5 seconds an alive message is sent to the bot to check if it's still there
        if get_millis() - start_time > 5000:
            print(timeout_counter)
            send_msg("a", address)
            start_time = get_millis()
            timeout_counter += 1
        
        try:
            data= sock.recv(1024)
        except:
            data = -1    
        
        if data == b"a":
            timeout_counter = 0
            print("Alive")
        
        
            

        
        


def start():
    print(f"[RUNNING] Server is running on {HOSTADDR}")
    while True:

        try:
            data,addr = sock.recvfrom(1024)
        except:
            data = -1
            addr = -1
        
        if data != -1:
            
            if data == b"w":
                if addr in address_list:
                    pass
                else:
                    address_list.append(addr)
                    thread = threading.Thread(target=handle_bot, args=(data, addr))
                    thread.start()
                    print(f"[TOTAL CONNECTIONS] {threading.activeCount() - 1}")
                    print(address_list)

print("[STARTING] Server is starting up...")
start()        
        
            

        
    
