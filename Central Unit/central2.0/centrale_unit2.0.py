#import keyboard 
from re import split
import time
import math
import socket
import numpy as np
import keyboard
#from myUDP import UDPsender,UDPreceiver
from Robot import Robot

UDP_IP = "192.168.11.192"
UDP_HOSTPORT = 1338

HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)

def calculate_distances(targets, pos):
    distances = []
    print(f"{targets}{pos}")
    for t_pos in targets:
        distances.append(math.sqrt(((t_pos[0]-pos[0])**2)+((t_pos[1]-pos[1])**2)))
    
    print(distances)
    return distances    
    
def calculate_degrees(bot):
    target = np.array(bot.target)
    current_pos = np.array(bot.position)
    origin = np.array([target[1],current_pos[1]])
    
    v0 = target - current_pos
    v1 = origin - current_pos
    
    #To calculate the angle to turn to the goal from 0 degrees
    angle = np.degrees(np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1)))

    #When the goal is in a different quadrant adjustments need to be made
    #these statements define the quadrants
    #if leftbehind
    if target[0] < current_pos[0] and target[1] < current_pos[1]:
        angle = angle + 180
    #if leftfront
    elif target[0] > current_pos[0] and target[1] < current_pos[1]:
        angle = angle + 180
    #if rightbehind
    elif target[0] < current_pos[0] and target[1] > current_pos[1]:
        angle = angle
        
    #if rightfront
    elif target[0] > current_pos[0] and target[1] > current_pos[1]:
        angle = angle
 
    #if target is directly behind
    elif current_pos[0] == target[0] and current_pos[1] > target[1]:
        angle = 180
    #if target is directly in front
    elif current_pos[0] == target[0] and current_pos[1] < target[1]:
        angle = 0
    #if target is directly to the left
    elif current_pos[1] == target[1] and current_pos[0] > target[0]:
        angle = 90
    #if target is directly to the right
    elif current_pos[1] == target[1] and current_pos[0] < target[0]:
        angle = -90

    return angle


#Dit moet anders of weg
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

def send_msg(message, address):
    print(f"[SENDING] Message: {message} to address {address}")
    sock.sendto(str(message).encode(), address)

def get_bot(bot_list, name):
    for bot in bot_list:
        if bot.name == name:
            return bot
        else:
            return None

def start():
    messages = []
    split_message = []
    bot_list = []
    address_list = []

    formation = []
    formation1 = [[0.25,0.25],[1.75,0.25],[0.25,1.75],[1.75,1.75]]
    formation2 = [[1.0,0.25],[0.25,1.0],[1.0,1.75],[1.75,1.0]]

    pick_formation = True
    formation_assigned = True
    targets_assigned = False
    #Counter for last message that is read
    last_message = 0

    while True:

        for bot in bot_list:
            #send_msg("fggt", bot.address)
            print(f"{bot.name}{bot.position}")

        #Path Planning should come down here I think
        if bot_list != [] and formation != [] and pick_formation == False and formation_assigned == True:
            #For all the robots in the list check which distance is closest and set that as a target
            #Later on there has to be a check for the other distances between all the robots
            #Maybe by using a distance list which keeps a list of all the distances
            for bot in bot_list:
                #Calculate distances for each bot
                distances = calculate_distances(formation, bot.position)
                #Check which is the smallest distance for each bot
                smallest_distance_index = distances.index(min(distances))
                #Set smallest distance as a target
                bot.target = formation[smallest_distance_index]
                #Calculate the angles for each point
                bot.target_heading = calculate_degrees(bot)
                send_msg(f"head#{bot.target_heading}", bot.address)

            formation_assigned = False
            targets_assigned = True

        #If the buffer is empty read any incoming messages
        if len(messages) <= last_message:
            with open("Messages.txt", 'r') as f:
                messages = f.readlines()
        
        #If there are any messages in the buffer that have not been read
        if len(messages) > last_message:
            #Parse incoming message into ('ip-address', port) and messages
            split_message = messages[last_message].strip('\n').split('#')
            
            #Get ip-address and port from message
            address_string = split_message[0].strip('()\'').split('\', ')
            address = (address_string[0], int(address_string[1]))

            command = split_message[1]
            name = split_message[2]
            

            #If the address isn't in the list add it to the list
            if address in address_list:
                bot = get_bot(bot_list, name)
                
                
                #Handle incoming commands here that are not 'wake' because the bots are already added
                if command == "pos":
                    data = split_message[3]
                    data = data.strip('\'[]\'').split(', ')
                    pos = [float(data[0]), float(data[1])]

                    bot.position = pos

                    #Hier moet je de bot verkrijgen van de naam en niet van de index

                    #When targets are assigned the bots will spam their location so that when they close to their target
                    #The Central Unit can say they need to stop driving
                    if targets_assigned:
                        #Check if the position has been reached with a margin of error
                        #This will be harder than expected
                        #You need to track again if the target is left/right behind/front
                        

                        #For all targets that every robot is assigned to
                        distance_to_target = bot.get_distance_to_target()
                        
                        if distance_to_target < 0.1:
                            send_msg("stop", bot.address)
                            bot.goal_achieved = True
                        
                        #if all(bot.goal_achieved):
                        #    targets_assigned = False
                        #    pick_formation = True
                        
            else:
                if command == 'wake':
                    if name == "camera":
                        address_list.append(address)
                    else:
                        bot = Robot(address, name)
                        bot_list.append(bot)
                        address_list.append(address)
            

            #Increment which message has been read last
            last_message += 1
            
        #When program is terminated delete everything in the file
        #And then close it
        if keyboard.is_pressed('q'):
            file = open("Messages.txt", 'w')
            file.truncate()
            file.close()
            break
        
        if keyboard.is_pressed('1') and pick_formation == True:
            formation = formation1
            print("[EXECUTING] Formation 1: Square")
            pick_formation = False
            formation_assigned = True
        if keyboard.is_pressed('2') and pick_formation == True:
            formation = formation2
            print("[EXECUTING] Formation 2: Diamond")
            pick_formation = False
            formation_assigned = True



print("[STARTING] Central Unit")
print("[INFO] To terminate press: q")
start()