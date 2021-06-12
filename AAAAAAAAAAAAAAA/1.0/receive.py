import socket
import keyboard

file = open(r"Messages.txt", "a+")


messages = []
UDP_IP = "127.0.0.1"
UDP_HOSTPORT = 1337

HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)
sock.settimeout(0)

def get_messages():
    return messages


def start():
    print(f"[RUNNING] Receiving server is running on {HOSTADDR}")
    cnt = 0
    while True:

        try:
            data,addr = sock.recvfrom(1024)
        except:
            data = -1
            addr = -1

        if data != -1:
            print(cnt)
            #print(f"{data},{addr}")
            messages.append(f"{addr}#{data.decode()}\n")
            file.write(f"{addr}#{data.decode()}\n")
            file.flush()
            cnt += 1

        if keyboard.is_pressed('SPACE'):
            file.close()
            break

print("[STARTING] Server is starting up...")
print("[INFO] To terminate press SPACEBAR")
start()