import keyboard 
import time
from myUDP import UDPsender,UDPreceiver

toRobot_1 = UDPsender("192.168.43.223",4210) # robot 


#sendPacket = UDPsender("224.0.1.3",4210)# sendPacket.send(b"f")
#receivePacket = UDPreceiver("224.0.1.3",4210)# receivePacket.receive(b"f")

"""  
commands 

toRobot_1.send(b"f")   #forward
toRobot_1.send(b"b")   #back
toRobot_1.send(b"r")   #right
toRobot_1.send(b"l")   #left


degrees = "90" #turn right 90 degrees
degrees = bytes(degrees, encoding='utf-8')
toRobot_1.send(degrees) 
"""


while True:

    if keyboard.is_pressed('UP'): 
            toRobot_1.send(b"f")
            print("f")
    elif keyboard.is_pressed('DOWN'):  
            toRobot_1.send(b"b");
            print("b")
    elif keyboard.is_pressed('RIGHT'): 
            toRobot_1.send(b"r");
            print("r")
    elif keyboard.is_pressed ('LEFT'): 
            toRobot_1.send(b"l");
            print("l")
    elif keyboard.is_pressed('g'):
            time.sleep(1)
            degrees = input("\n insert: ") # for example 90
            degrees = bytes(degrees, encoding='utf-8')

            toRobot_1.send(degrees)
            print("rotating")
    elif keyboard.is_pressed('SPACE'): 
            toRobot_1.send(b"s");
            print("SPACE")

    time.sleep(0.05)