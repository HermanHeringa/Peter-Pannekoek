import socket
import keyboard

file = open(r"Messages.txt", "a+")


messages = []

#Define IP-address and port
UDP_IP = "127.0.0.1"
UDP_HOSTPORT = 1337
HOSTADDR = (UDP_IP, UDP_HOSTPORT)

#Open up connection on IP-address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)
sock.settimeout(0)

#Function to get messages list
def get_messages():
    return messages

def start():
    print(f"[RUNNING] Receiving server is running on {HOSTADDR}")

    while True:

        #Try to receive any incoming data
        try:
            data, addr = sock.recvfrom(1024)
        except Exception:
            data = -1
            addr = -1

        #If there is data write the address and the data to the file
        if data != -1:
            messages.append(f"{addr}#{data.decode()}\n")
            file.write(f"{addr}#{data.decode()}\n")
            file.flush()

        #When the program has to quit delete the Messages.txt cache
        if keyboard.is_pressed('q'):
            f = open("Messages.txt", 'w')
            f.truncate()
            f.close()
            break


print("[STARTING] Server is starting up...")
print("[INFO] To terminate press q")
start()
