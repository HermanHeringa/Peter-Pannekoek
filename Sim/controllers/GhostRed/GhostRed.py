"""Ghost1 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor
import socket

TIME_STEP = 16
MAX_SPEED = 1
UDP_IP = "127.0.0.1"
UDP_PORT = 4210
UDP_HOSTPORT = 1337
ADDR = (UDP_IP, UDP_PORT)
HOSTADDR = (UDP_IP, UDP_HOSTPORT)
BOT_NAME = "ghost-red"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0)

# create the Robot instance.
robot = Supervisor()
supervisorNode = robot.getSelf()
trans = supervisorNode.getField("translation")
# target = supervisorNode.getField("target")
pos = trans.getSFVec3f() # get de translation


def send_msg(message):
    print(message)
    sock.sendto(str(message).encode(), HOSTADDR)


def moveRobot(pos_):
    _, posY, _ = supervisorNode.getPosition()

    newX, newZ = pos_

    new_pos = [newX, posY, newZ]

    trans.setSFVec3f(new_pos)


def start():
    while robot.step(TIME_STEP) != -1:

        try:
            data, addr = sock.recvfrom(1024)
        except (ValueError, Exception):
            data = -1
            addr = -1

        if data != -1:

            data = data.decode().split("#")
            command = data[0]

            print(f"{BOT_NAME} {data}")

            if command == "newPos":
                pos = data[1]
                pos = pos.strip('\'[]\'').split(', ')
                pos = [float(pos[0]), float(pos[1])]
                moveRobot(pos)
                # split the received
                # pos[0]= x
                # pos[2]= z (we use x and z in webots)


send_msg(f"wake#{BOT_NAME}")
start()
