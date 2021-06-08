import keyboard 
import time
from myUDP import UDPsocket

packet = UDPsocket("192.168.43.223",4210) # Network ip and port
	 
while True:
    if keyboard.is_pressed('UP'): 
            packet.send(b"f")
            print("f")
    elif keyboard.is_pressed('DOWN'): 
            packet.send(b"b");
            print("b")
    elif keyboard.is_pressed('RIGHT'): 
            packet.send(b"r");
            print("r")
    elif keyboard.is_pressed('LEFT'): 
            packet.send(b"l");
            print("l")
    elif keyboard.is_pressed('SPACE'): 
            packet.send(b"s");
            print("SPACE")
    time.sleep(0.1)