import socket

HEADER = 64
PORT = 1337
SERVER = "192.168.11.193"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "CLOSE"

websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: Websocket',
    'Connection: upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)
handshake_msg = (
    'GET / HTTP/1.1\n'
    'Host: 192.168.11.193\n'
    'Sec-WebSocket-Key: MDEyMzQ1Njc4OWFiY2RlZg==\n'
    'Upgrade: websocket\n'
    'Connection: Upgrade\n'
    'Sec-WebSocket-Version: 13\n'
    'User-Agent: TinyWebsockets Client\n'
    'Origin: https://github.com/gilmaimon/TinyWebsockets\n'
)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    
print(handshake_msg)    
send(handshake_msg)
print(client.recv(2048).decode(FORMAT))
send("ROBIN IS DIK")
print(client.recv(2048).decode(FORMAT))
send("THOM HEEFT EEN GROOTHOOFD")
print(client.recv(2048).decode(FORMAT))
send("JAAPIE IS EEN HACKER")
print(client.recv(2048).decode(FORMAT))
send("MICKEY MOUSE")
print(client.recv(2048).decode(FORMAT))

client.close()