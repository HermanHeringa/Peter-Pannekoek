from re import split
import socket
import keyboard
import numpy as np
import math

UDP_IP = "127.0.0.1"
UDP_HOSTPORT = 1338

HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)

def calculate_distances(targets, pos):
    distances = []
    
    for t_pos in targets:
        distances.append(math.sqrt(((t_pos[0]-pos[0])**2)+((t_pos[1]-pos[1])**2)))
    
    return distances


def calculate_degrees(tgt, pos):
    target = np.array(tgt)
    current_pos = np.array(pos)
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
        
def send_msg(message, address):
    print(f"[SENDING] Message: {message} to address {address}")
    sock.sendto(str(message).encode(), address)

def start():
    #Define buffer for messages
    messages = []
    split_message = []
    
    address_list = []
    bot_list = []
    position_list = []
    angles = []
    targets = []
    goal_achieved = []

    formation = []
    formation1 = [[0.25,0.25],[1.75,0.25],[0.25,1.75],[1.75,1.75]]
    formation2 = [[1.0,0.25],[0.25,1.0],[1.0,1.75],[1.75,1.0]]
    
    pick_formation = True
    formation_assigned = True
    targets_assigned = False
    #Counter for last message that is read
    last_message = 0
    

    while True:
        
        #Path Planning should come down here I think
        if bot_list != [] and formation != [] and pick_formation == False and formation_assigned == True:
            #For all the robots in the list check which distance is closest and set that as a target
            #Later on there has to be a check for the other distances between all the robots
            #Maybe by using a distance list which keeps a list of all the distances
            for bot in range(len(bot_list)):
                #Calculate distances for each bot
                distances = calculate_distances(formation, position_list[bot])
                #Check which is the smallest distance for each bot
                smallest_distance_index = distances.index(min(distances))
                #Set smallest distance as a target
                target_pos = formation[smallest_distance_index]
                targets[bot] = target_pos
                #Calculate the angles for each point
                angles[bot] = calculate_degrees(targets[bot], position_list[bot])
                send_msg(f"head#{angles[bot]}", address_list[bot])
            
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
            data = split_message[2]

            #If the address isn't in the list add it to the list
            if address in address_list:
                index = address_list.index(address)
                
                #Handle incoming commands here that are not 'wake' because the bots are already added
                if command == "pos":
                    
                    #If the position is given by the camera or webots update this in the position list
                    data = data.strip('\'[]\'').split(', ')
                    pos = [float(data[0]), float(data[1])]
                    position_list[index] = pos
                    
                    #When targets are assigned the bots will spam their location so that when they close to their target
                    #The Central Unit can say they need to stop driving
                    if targets_assigned:
                        #Check if the position has been reached with a margin of error
                        #This will be harder than expected
                        #You need to track again if the target is left/right behind/front
                        target = [targets[index]]


                        #For all targets that every robot is assigned to
                        distance_to_target = calculate_distances(target, pos)
                        
                        if distance_to_target[0] < 0.1:
                            send_msg("stop", address_list[index])
                            goal_achieved[index] = True
                        
                        if all(goal_achieved):
                            targets_assigned = False
                            pick_formation = True
                        
            else:
                if command == 'wake':
                    position_list.append([0.0,0.0])
                    angles.append(0)
                    targets.append([0.0,0.0])
                    goal_achieved.append(False)
                    address_list.append(address)
                    bot_list.append(data)
                    send_msg("pos", address)
        
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