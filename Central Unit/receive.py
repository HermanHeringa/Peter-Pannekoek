import socket
import keyboard

file = open(r"Messages.txt", "a+")


messages = []
UDP_IP = "192.168.137.1"
UDP_HOSTPORT = 1337

HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)
sock.settimeout(0)


def get_messages():
    return messages


def start():
    print(f"[RUNNING] Receiving server is running on {HOSTADDR}")

    while True:

        try:
            data, addr = sock.recvfrom(1024)
        except Exception:
            data = -1
            addr = -1

        if data != -1:
            messages.append(f"{addr}#{data.decode()}\n")
            file.write(f"{addr}#{data.decode()}\n")
            file.flush()

        if keyboard.is_pressed('q'):
            f = open("Messages.txt", 'w')
            f.truncate()
            f.close()
            break


print("[STARTING] Server is starting up...")
print("[INFO] To terminate press q")
start()
