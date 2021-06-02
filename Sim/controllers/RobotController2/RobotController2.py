from controller import Robot, Motor, Compass, GPS
import math
import socket


TIME_STEP = 16

MAX_SPEED = 1
UDP_IP = "192.168.11.193"
UDP_PORT = 4211
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
    run_motor(0.1,0.1)

def backward():
    run_motor(-0.1,-0.1)

def left():
    run_motor(-0.1,0.1)

def right():
    run_motor(0.1,-0.1)
    
def stop():
    run_motor(0.0,0.0)
    
#Function to turn into right direction
def turn(degrees):
    pass




def start():    
    while robot.step(TIME_STEP) != -1:
                  
            try:
                data,addr = sock.recvfrom(1024)
            except:
                data = -1
                addr = -1
            if data != -1:
            
                print(data)
                print(addr)
                
                if data == b"f":
                    send_msg(-1)
                    forward()
                elif data == b"b":
                    send_msg(-1)
                    backward()
                elif data == b"l":
                    send_msg(-1)   
                    left()
                elif data == b"r":
                    send_msg(-1)
                    right()
                elif data == b"s":
                    send_msg(-1)
                    stop()
                elif data == b"h":
                    heading = get_bearing_in_degrees()
                    send_msg(heading)
                elif data == b"p":
                    pos = get_pos()
                    send_msg(pos)
                    
                data = -1
               
#Setup
heading = get_bearing_in_degrees()
pos = get_pos()
start()
    