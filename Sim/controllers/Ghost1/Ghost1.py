"""Ghost1 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor
import socket

TIME_STEP = 16
MAX_SPEED = 1
UDP_IP = "192.168.137.1"
UDP_PORT = 4210
UDP_HOSTPORT = 1337
ADDR = (UDP_IP,UDP_PORT)
HOSTADDR = (UDP_IP, UDP_HOSTPORT)
BOT_NAME = "ghost1"

# create the Robot instance.
robot = Supervisor()
supervisorNode = robot.getSelf()
trans = supervisorNode.getField("translation")
#target = supervisorNode.getField("target")
pos = trans.getSFVec3f() #get de translation

def send_msg(message):
    print(message)
    sock.sendto(str(message).encode(), HOSTADDR)

def receive_msg(message):
    #to do
    pass

    
def start():
    #wahedWaar = True
    wahedWaar2 = False
    while robot.step(TIME_STEP) != -1:
        
        try:
            data,addr = sock.recvfrom(1024)
        except:
            data = -1
            addr = -1
        
        if data != -1:
            
            data = data.decode().split("#")
            command = data[0]
            
            if command == "newPos":
                #split de received
                #pos[0]= x
                #pos[2]= z (wij gebruiken x en z in webots)
                #trans.setSFVec3f(pos) #om de nieuw positie te zetten als het goed is
                                                
send_msg(f"wake#{BOT_NAME}")
start()
    