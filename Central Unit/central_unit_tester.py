#import keyboard 
import time
import math
import numpy as np
import keyboard
from myUDP import UDPsender,UDPreceiver

toRobot = UDPsender("192.168.43.223",4210) # Network ip and port
#fromRobot_1 = UDPreceiver("192.168.137.1",4210)# Host_ip in arduino code, each robot has its own host IP
#fromRobot_1.receive()



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
    

def calculate_degrees(pos):
    current_pos = np.array([1.0 , 1.0])
    origin = np.array([pos[0],current_pos[1]])
   # print(f" curpos {current_pos}")
   # print(f" pos {pos}")
   # print(f" origin {origin}")
    
    v0 = current_pos - pos
    v1 = origin - pos
    
    #to calculate the angle to turn to the goal from 0 degrees
    angle = np.degrees(np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1)))
    #print(angle)
    
    #When the goal is in a different quadrant adjustments need to be made
    #these statements define the quadrants
    #if leftbehind
    if pos[0] < current_pos[0] and pos[1] < current_pos[1]:
        angle = 180.0 - angle
    #if leftfront
    elif pos[0] < current_pos[0] and pos[1] > current_pos[1]:
        angle = angle * -1.0
    #if rightbehind
    elif pos[0] > current_pos[0] and pos[1] < current_pos[1]:
        angle = 180.0 - angle - 360 
    #if rightfront
    elif pos[0] > current_pos[0] and pos[1] > current_pos[1]:
        angle = angle * -1.0
 
    #if target is directly behind
    elif current_pos[0] == pos[0] and current_pos[1] > pos[1]:
        angle = 180
    #if target is directly in front
    elif current_pos[0] == pos[0] and current_pos[1] < pos[1]:
        angle = 0
    #if target is directly to the left
    elif current_pos[1] == pos[1] and current_pos[0] > pos[0]:
        angle = 90
    #if target is directly to the right
    elif current_pos[1] == pos[1] and current_pos[0] < pos[0]:
        angle = -90
    #print(angle)
    return angle

def assign_goal(target):
    #targetpos = np.array([1.0,1.75]) #testing purpose
    targetheading = calculate_degrees(target)
    #we split the targetheading into postives and negatives to later specify which wat to turn to
    if targetheading > 180:
        targetheading = targetheading - 360
    dest_heading = 360 - targetheading
        #to make sure we stay in the first circle only we subtract 360 degrees when we go over the 360
    if dest_heading > 360:
        dest_heading = dest_heading - 360
 
apos = [1.7, 0.8]
#h = calculate_degrees(apos)
h = np.float64(90.0)
print(type(h))
print(h)
toRobot.send(h)

while True:

    if keyboard.is_pressed('UP'): 
            toRobot.send(b"f")
            print("f")
    elif keyboard.is_pressed('DOWN'):  
            toRobot.send(b"b");
            print("b") 
    elif keyboard.is_pressed('RIGHT'): 
            toRobot.send(b"r");
            print("r")
    elif keyboard.is_pressed('LEFT'): 
            toRobot.send(b"l");
            print("l")
    elif keyboard.is_pressed('SPACE'): 
            toRobot.send(b"s");
            print("SPACE")
    elif keyboard.is_pressed('g'):
        h = f"{h}"
        toRobot.send(h.encode('utf-8'))
        print("g")

    time.sleep(0.1)