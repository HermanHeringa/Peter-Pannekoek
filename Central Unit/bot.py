from controller import Robot, Motor, Compass
import math
import socket


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
compass.enable(250)

def get_bearing_in_degrees():
    north = compass.getValues()
    rad = math.atan2(north[0], north[2])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if (bearing < 0.0):
        bearing = bearing + 360.0
    return bearing

def run_motor(left, right):
    leftMotor = robot.getDevice('LeftMotor')
    rightMotor = robot.getDevice('RightMotor')
    
    # get a handler to the motors and set target position to infinity (speed control)   
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    
    #set up the motor speeds at 10% of the MAX_SPEED.
    leftMotor.setVelocity(left * MAX_SPEED)
    rightMotor.setVelocity(right * MAX_SPEED) 

def forward():
    run_motor(0.5,0.5)

def backward():
    run_motor(-0.5,-0.5)

def left():
    run_motor(-0.5,0.5)

def right():
    run_motor(0.5,-0.5)
    
def stop():
    run_motor(0.0,0.0)
    
while robot.step(TIME_STEP) != -1:
        heading = get_bearing_in_degrees()
        print(heading)
        try:
            data,addr = sock.recvfrom(1024)
        except:
            data = -1
            addr = -1
        if data != -1:
        
            print(data)
            print(addr)
            
            if data == b"f":
                forward()
            elif data == b"b":
                backward()
            elif data == b"l":   
                left()
            elif data == b"r":
                right()
            elif data == b"s":
                stop()
            elif data == b"h":
                sock.sendto(str(heading).encode(), HOSTADDR)
                pass
            data = -1
            
        pass
    