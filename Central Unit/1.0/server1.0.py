import socket
import re
import threading
import base64
from hashlib import sha1

HEADER = 1024
PORT = 1337
HOST = "192.168.11.193" #socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

RECEIVED_MESSAGE = "ACK"
DISCONNECT_MESSAGE = "CLOSE"

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: Websocket',
    'Connection: upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def close_connection(client):
    client.close()

def send_msg(client, msg):
    client.send(msg.encode(FORMAT))
    print(msg)

def do_handshake(client):
    msg = client.recv(HEADER).decode(FORMAT)

    print(f"[HANDSHAKE] {msg}")
        
    key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', msg)
    .groups()[0]
    .strip())

    response_key = base64.b64encode(sha1((key + GUID).encode(FORMAT)).digest())
    response = '\r\n'.join(websocket_answer).format(key=response_key.decode(FORMAT))

    print(response)
    send_msg(client, response)
    send_msg(client, "test")

def handle_client(client, address):
    print(f"[NEW CONNECTION] Client connected on: {address}")

    do_handshake(client)

    connected = True
    while connected:
        send_msg(client, "aaaa")
        msg = client.recv(HEADER)
        
        if msg != -1:
            
            print(type(msg))
            print(f"[{address}] {msg}")
            client.send(msg)
        #send_msg(client, RECEIVED_MESSAGE)    

    print(f"[CLOSING] Closing connection with client on {address}")
    #send_msg(client, DISCONNECT_MESSAGE)    
    client.close()
    

def start():
    server.listen()
    print(f"[RUNNING] Server is running on {HOST}:{PORT}")
    
    while True:
        client, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()
        print(f"[TOTAL CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Server is starting up")
start()