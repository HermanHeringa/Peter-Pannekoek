import keyboard 
import time
from myUDP import UDPsender,UDPreceiver

packet = UDPsender("192.168.43.70",4210) # Network ip and port
fromRobot_1 = UDPreceiver("224.0.1.3",4210)# Host_ip in arduino code, each robot has its own host IP
fromRobot_1.receive()

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