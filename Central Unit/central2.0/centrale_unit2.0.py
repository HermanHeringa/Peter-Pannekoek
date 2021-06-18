#import keyboard 
from re import split
from scipy.optimize import linear_sum_assignment
import time
import math
import socket
import numpy as np
import keyboard
#from myUDP import UDPsender,UDPreceiver
from Robot import Robot

UDP_IP = "192.168.137.1"
UDP_HOSTPORT = 1338

HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)

def calculate_distances(targets, bot_list):
    
    for bot in bot_list:
        pos = bot.position
        target_distances = []
        for t_pos in targets:
            target_distances.append(math.sqrt(((t_pos[0]-pos[0])**2)+((t_pos[1]-pos[1])**2)))
        bot.distance_to_targets = target_distances
        #print(bot.distance_to_targets)

def get_targets(bot_list):
    distances = []
    for bot in bot_list:
        #print(bot.distance_to_targets)
        distances.append(bot.distance_to_targets)
    
    cost = np.array(distances)
    #print(cost)

    return linear_sum_assignment(cost)

def calculate_degrees(position, target):
    deltaX = target[0] - position[0]
    deltaY = target[1] - position[1]
    return -round(np.degrees(np.math.atan2(deltaY, deltaX)))

def send_msg(message, address):
    print(f"[SENDING] Message: {message} to address {address}")
    sock.sendto(str(message).encode(), address)

def get_bot(bot_list, name):
    #bot = Robot(("0.0.0.0", 1337), "empty")
    for _bot in bot_list:
        
        if _bot.name == name:
            bot = _bot
            return bot
    

    
def start():
    bot = None

    messages = []
    split_message = []
    bot_list = []
    address_list = []

    formation = []
    formation1 = [[0.25,0.25],[1.75,0.25],[0.25,1.75],[1.75,1.75]]
    formation2 = [[1.1,0.25],[0.25,1.1],[1.1,1.75],[1.75,1.1]]

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
            #for bot in bot_list:
                #Calculate distances for each bot
            calculate_distances(formation, bot_list)

            target_index = get_targets(bot_list)[1].tolist()
            #print(target_index)

            #Voor elke item in target_index assign de robot zijn target via formation[target_index]
            for index in target_index:
                bot = bot_list[target_index.index(index)]
                bot.target = formation[index]
                # bot0: 0 bot1: 2 bot3: 1 bot4:3

                #Calculate the angles for each point
                bot.target_heading = calculate_degrees(bot.position, bot.target)
                send_msg(f"head#{bot.target_heading}", bot.address)

                #for bot in bot_list:
                    #send_msg("head#12345", bot.address)
                    #print(f"{bot.name}{bot.target}")

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
                
                
                #Handle incoming commands here that are not 'wake' because the bots are already added
                if command == "pos":
                    data = split_message[3]
                    data = data.strip('\'[]\'').split(', ')
                    pos = [float(data[0]), float(data[1])]
                    
                    bot = get_bot(bot_list, name)

                    if bot != None:
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
                        send_msg(f"head#135", address)
                print(f"{command}, {name}")
            

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