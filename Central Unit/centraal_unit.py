#import keyboard 
import time
import math
from myUDP import UDPsender,UDPreceiver

packet = UDPsender("192.168.43.70",4210) # Network ip and port
fromRobot_1 = UDPreceiver("224.0.1.3",4210)# Host_ip in arduino code, each robot has its own host IP
fromRobot_1.receive()

def calculate_distance(pos1, pos2):
        x1 = pos1[0]
        x2 = pos2[0]
        y1 = pos1[1]
        y2 = pos2[1]
        distance = math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        return distance

#calculate_distance test, output should be 1.41 with pos1[2,2] and pos2[3,3]
#pos1 = [2,2]
#pos2 = [3,3]
#print(calculate_distance(pos1, pos2))

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