from controller import Robot, Motor, Compass
import math



TIME_STEP = 16

MAX_SPEED = 1



# create the Robot instance.
robot = Robot()
compass = Compass("compass")
compass.enable(250)

# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('LeftMotor')
rightMotor = robot.getDevice('RightMotor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))



# set up the motor speeds at 10% of the MAX_SPEED.
leftMotor.setVelocity(0.05 * MAX_SPEED)
rightMotor.setVelocity(0.01 * MAX_SPEED)

def get_bearing_in_degrees():
    north = compass.getValues()
    rad = math.atan2(north[0], north[2])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if (bearing < 0.0):
        bearing = bearing + 360.0
    return bearing



while robot.step(TIME_STEP) != -1:
    
    print(get_bearing_in_degrees())
    pass