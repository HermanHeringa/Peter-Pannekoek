from controller import Robot, Motor, Compass, GPS
import math
import socket

TIME_STEP = 16

MAX_SPEED = 1
UDP_IP = "127.0.0.1"
UDP_PORT = 4210
UDP_HOSTPORT = 1337
ADDR = (UDP_IP, UDP_PORT)
HOSTADDR = (UDP_IP, UDP_HOSTPORT)

BOT_NAME = "blue"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
    # calculate the bearing/heading
    north = compass.getValues()
    rad = math.atan2(north[0], north[2])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if bearing < 0.0:
        bearing = bearing + 360.0
    return bearing


def get_pos():
    xyz = gps.getValues()  # Get XYZ Values from GPS Module
    xyz.pop(1)  # Remove Y value because it is not needed
    # xyz = [ round(elem, 2) for elem in xyz]
    return xyz  # Return X and Z values


def run_motor(left_, right_):
    leftMotor = robot.getDevice('LeftMotor')
    rightMotor = robot.getDevice('RightMotor')

    # get a handler to the motors and set target position to infinity (speed control)
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))

    # set up the motor speeds at 10% of the MAX_SPEED.
    leftMotor.setVelocity(left_ * MAX_SPEED)
    rightMotor.setVelocity(right_ * MAX_SPEED)


# Functions defining movement and speed
def forward():
    run_motor(0.05, 0.05)


def backward():
    run_motor(-0.05, -0.05)


def left():
    run_motor(-0.05, 0.05)


def right():
    run_motor(0.05, -0.05)


def stop():
    run_motor(0.0, 0.0)


def start():
    first_loop = False
    target_received = False
    while robot.step(TIME_STEP) != -1:

        try:
            data, addr = sock.recvfrom(1024)
        except (ValueError, Exception):
            data = -1
            addr = -1

        if data != -1:

            data = data.decode().split("#")

            command = data[0]

            if command == "head":
                target_heading = float(data[1])
                first_loop = True
                target_received = True
            elif command == "stop":
                stop()
                target_received = False

        if target_received:
            # only assign the goal once and calculate how much degrees to turn from the 0 point
            # if you repeat these calculations the degrees to turn from the 0 point will shift
            if first_loop:
                print(f"target heading: {target_heading}")
                # we split the targetheading into postives and negatives to later specify which wat to turn to
                if target_heading > 180:
                    target_heading = target_heading - 360
                elif target_heading < -180:
                    target_heading = target_heading + 360

            # get the angle of the bot compared to the simulated magnetic north
            current_angle = get_bearing_in_degrees()

            # only calculate the destination heading once so that it won't shift
            if first_loop:
                dest_heading = 360 - target_heading
                # to make sure we stay in the first circle only we subtract 360 degrees when we go over the 360
                if dest_heading > 360:
                    dest_heading = dest_heading - 360
                print(f"dest angle: {dest_heading}")
                print(f"current angle: {current_angle}")
                first_loop = False

            # we constantly calculate the angle error.
            # this the difference between it's current angle and the destinations angle
            angle_error = current_angle - dest_heading
            print(f"error: {angle_error}")
            print(f"current angle: {current_angle}")

            # intiate the turn if we are not currently looking at the destinations heading
            # because the robot is not 100% accurate we give it a slight error zone of 2 degrees
            if current_angle != dest_heading and angle_error > 2 or angle_error < -2:
                # here we choose which side to turn to.
                # because we split the targetheading in 2 sides we can do it simply by looking if it is negative or positive
                if target_heading > 0:
                    left()
                else:
                    right()
            else:
                forward()

        send_msg(f"pos#{BOT_NAME}#{get_pos()}")


# Setup
heading = get_bearing_in_degrees()
pos = get_pos()
send_msg(f"wake#{BOT_NAME}")
start()
