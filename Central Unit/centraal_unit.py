#import keyboard 
import time
import math
from myUDP import UDPsender,UDPreceiver

packet = UDPsender("192.168.43.70",4210) # Network ip and port
fromRobot_1 = UDPreceiver("224.0.1.3",4210)# Host_ip in arduino code, each robot has its own host IP
fromRobot_1.receive()

robot1 = Robot(90, "blue", "192.168.1.2", "224.0.1.3")
robot2 = Robot(180, "red", "192.168.1.3", "224.0.1.4")
robot3 = Robot(270, "green", "192.168.1.4", "224.0.1.5")
robot4 = Robot(360, "sim", "192.168.1.5", "224.0.1.6")

class Robot():
    target = null
    targetheading = null
    def __init__(heading, color, ip, host_ip):
        self.heading = heading
        self.color = color
        self.ip = ip
        self.robotreceiver = UDPreceiver(host_ip, 4210)
        self.robotsender = UDPsender(ip, 4210)
                
    def set_target(self, target):
        self.target = target
        
    def set_target_heading(self, targetheading):
        self.targetheading = targetheading
    
    def get_pos(self):
        #to do
        return null
        
    def get_heading(self):
        return self.robotreceiver.receive()
    
    def get_target_heading(self):
        return self.targetheading

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
    current_pos = np.array(get_pos())
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