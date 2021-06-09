from controller import Robot, Motor, Compass, GPS
import math
import socket
import numpy as np
#IMPORTENT#
#this is a variation to RobotController1 from 8/6/21
#the goal was to develop a simpler version to turn the robot

TIME_STEP = 16

MAX_SPEED = 1
UDP_IP = "127.0.0.1"
UDP_PORT = 4210
UDP_HOSTPORT = 1337
ADDR = (UDP_IP,UDP_PORT)
HOSTADDR = (UDP_IP, UDP_HOSTPORT)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR)
sock.settimeout(0)

# create the Robot instance.
robot = Robot()
compass = Compass("compass")
gps = GPS("gps")

compass.enable(1)
gps.enable(1)

def send_msg(message):
    print(message)
    sock.sendto(str(message).encode(), HOSTADDR)

def get_bearing_in_degrees():
    north = compass.getValues()
    rad = math.atan2(north[0], north[2])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if (bearing < 0.0):
        bearing = bearing + 360.0
    return bearing

def get_pos():
    xyz = gps.getValues() #Get XYZ Values from GPS Module
    xyz.pop(1)            #Remove Y value because it is not needed
    xyz = [ round(elem, 2) for elem in xyz]
    return xyz            #Return X and Z values
    
def run_motor(left, right):
    leftMotor = robot.getDevice('LeftMotor')
    rightMotor = robot.getDevice('RightMotor')
    
    # get a handler to the motors and set target position to infinity (speed control)   
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    
    #set up the motor speeds at 10% of the MAX_SPEED.
    leftMotor.setVelocity(left * MAX_SPEED)
    rightMotor.setVelocity(right * MAX_SPEED) 

#Functions defining movement and speed
def forward():
    run_motor(0.05,0.05)

def backward():
    run_motor(-0.05,-0.05)

def left():
    run_motor(-0.05,0.05)

def right():
    run_motor(0.05,-0.05)
    
def stop():
    run_motor(0.0,0.0)
    
#Function to turn into right direction
def turn(degrees):
    pass

def calculate_degrees(pos):
    current_pos = np.array(get_pos())
    origin = np.array([pos[0],current_pos[1]])
   # print(f" curpos {current_pos}")
   # print(f" pos {pos}")
   # print(f" origin {origin}")
    
    v0 = current_pos - pos
    v1 = origin - pos
    
    angle = np.degrees(np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1)))
    
    #print(angle)
    
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
        
        
        
def start():

    send_msg("w")
    wahedWaar = True
    
    while robot.step(TIME_STEP) != -1:
   
        if wahedWaar:
            targetpos = np.array([1.5,1.0])
            targetheading = calculate_degrees(targetpos)
            print(f"target heading: {targetheading}")
            if targetheading > 180:
                targetheading = targetheading - 360

        current_angle = get_bearing_in_degrees()
        
        
        if wahedWaar:
            dest_heading = 360 - targetheading
            if dest_heading > 360:
                dest_heading = dest_heading - 360
            print(f"dest angle: {dest_heading}")
            print(f"current angle: {current_angle}")
            wahedWaar = False
        
        angle_error = current_angle - dest_heading
        print (f"error: {angle_error}")
        print(f"current angle: {current_angle}")
        
        
        
        if current_angle != dest_heading and angle_error > 2 or angle_error < -2 :
            if targetheading > 0:
                left()
            else: 
                right()  
        else:
             forward()
            
        #current_angle = get_bearing_in_degrees()
            #targetheading = calculate_degrees(targetpos)
            #if angle_error >= 0 and targetheading > 0:
             #   left()
            #elif angle_error < 0:
             #   right()  
        
               
#Setup
heading = get_bearing_in_degrees()
pos = get_pos()
start()
    