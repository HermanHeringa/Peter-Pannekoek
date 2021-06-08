from controller import Robot, Motor, Compass, GPS
import math
import socket
import numpy as np


TIME_STEP = 16

MAX_SPEED = 1
UDP_IP = "192.168.11.193"
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
    print(f" curpos {current_pos}")
    print(f" pos {pos}")
    print(f" origin {origin}")
    
    v0 = origin - current_pos
    v1 = pos - current_pos
    
    angle = np.degrees(np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1)))
    
    print(angle)
    
    #if leftbehind
    if pos[0] < current_pos[0] and pos[1] < current_pos[1]:
        angle = 180.0 - angle
    #if leftfront
    elif pos[0] < current_pos[0] and pos[1] > current_pos[1]:
        angle = angle * -1.0
    #if rightbehind
    elif pos[0] > current_pos[0] and pos[1] < current_pos[1]:
        angle = 180.0 - angle
    
    #if rightfront
    elif pos[0] > current_pos[0] and pos[1] > current_pos[1]:
        angle = angle * -1.0
    
    print(angle)
    return angle
        
        
        
def start():

    send_msg("w")
    
    while robot.step(TIME_STEP) != -1:
        targetpos = np.array([0.0,2.0])
        targetheading = calculate_degrees(targetpos)
        #targetheading = -20.0
        
        
        
        
        start_angle = get_bearing_in_degrees()
        current_angle = start_angle
        
        if current_angle != ((start_angle + targetheading) % 360 ):
            print(current_angle)
            print(current_angle + targetheading)
            if current_angle > ((current_angle + targetheading) % 360):
                #print("a")
                left()
            elif current_angle < ((current_angle + targetheading) % 360):
                #print("b")
                right()
            else:
                stop()
            
            current_angle = get_bearing_in_degrees()
            #targetheading = calculate_degrees(targetpos)
            
        
               
#Setup
heading = get_bearing_in_degrees()
pos = get_pos()
start()
    