from controller import Robot, Motor, Compass
import math



TIME_STEP = 16

MAX_SPEED = 1



# create the Robot instance.
robot = Robot()
# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('LeftMotor')
rightMotor = robot.getDevice('RightMotor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))



# set up the motor speeds at 10% of the MAX_SPEED.
leftMotor.setVelocity(0.05 * MAX_SPEED)
rightMotor.setVelocity(0.01 * MAX_SPEED)




while robot.step(TIME_STEP) != -1:
    pass