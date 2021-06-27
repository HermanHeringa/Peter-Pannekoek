from scipy.optimize import linear_sum_assignment
import math
import socket
import numpy as np
import keyboard
from Robot import Robot
from GhostBot import Ghostbot

#Define IP-address and port
UDP_IP = "127.0.0.1"
UDP_HOSTPORT = 1338
HOSTADDR = (UDP_IP, UDP_HOSTPORT)

#Open up sockets on defined IP-address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(HOSTADDR)

#Function to calculate distances between all of the robots in the list and all of the targets
#It creates a list of "costs" to every target so that we can use it later to calculate priority
#for target assignment
def calculate_distances(targets, bot_list):
    for bot in bot_list:
        pos = bot.position
        target_distances = []
        for t_pos in targets:
            target_distances.append(math.sqrt(((t_pos[0]-pos[0])**2)+((t_pos[1]-pos[1])**2)))
        bot.distance_to_targets = target_distances

#This function creates the matrix of costs to every target for every bot
#It then finds the targets for every bot
#This will be an array of indexes of the "formation list" for each bot
def get_targets(bot_list):
    distances = []
    for bot in bot_list:
        distances.append(bot.distance_to_targets)
    
    cost = np.array(distances)

    return linear_sum_assignment(cost)

#This function returns the angle between the position of the robot and the assigned target
def calculate_degrees(position, target):
    deltaX = target[0] - position[0]
    deltaY = target[1] - position[1]
    return -round(float(np.degrees(np.math.atan2(deltaY, deltaX))))  # Casting to float first seems redundant, but IDE throws a warning if you don't

#This function is to send a command to the robot
def send_msg(message, address):
    print(f"[SENDING] Message: {message} to address {address}")
    sock.sendto(str(message).encode(), address)

#The function returns the bot with the same name as the name given
#This is used so we can get the correct bot to put incoming position data in
def get_bot(bot_list, name):
    for _bot in bot_list:
        if _bot.name == name:
            return _bot

#To make the ghosts in the simulation be at the same spot as the hardware robots
#We have to link these two together. This function returns the linked robot if there is any
def get_linked_bot(ghost_list, linked_bot):
    for _ghost in ghost_list:
        if _ghost.linked_bot == linked_bot:
            return _ghost
    

def start():
    #Definition of field
    field_width = 1.92
    field_height = 1.08
    side_margin = 0.2

    #Definition of used lists
    messages = []
    bot_list = []
    address_list = []

    #This is for the ghosts in webots
    ghosts_connected = 0
    ghost_list = []

    #Definition of the formations we created
    formation = []
    #Formation 1 is a Square over the field
    formation1 = [[side_margin, side_margin],
                  [field_width - side_margin, side_margin],
                  [side_margin, field_height - side_margin],
                  [field_width - side_margin, field_height - side_margin]]
    #Formation 2 is a Diamon spread across the field
    formation2 = [[field_width/2, side_margin],
                  [side_margin, field_height/2],
                  [field_width/2, field_height-side_margin],
                  [field_width-side_margin, field_height/2]]
    #Formation 3 is a Triangle
    formation3 = [[side_margin, side_margin], 
                  [field_width/2, side_margin],
                  [field_width-side_margin, side_margin],
                  [field_width/2, field_height-side_margin]]

    #Definition of booleans
    pick_formation = True
    formation_assigned = True
    targets_assigned = False
    # Counter for last message that is read
    last_message = 0

    while True:
        #If there are any bots and a formation is picked it will run all of the code to calculate the targets, headings, etc.
        if bot_list != [] and formation != [] and pick_formation is False and formation_assigned is True:
            # For all the robots in the list check which distance is closest and set that as a target
            calculate_distances(formation, bot_list)

            target_index = get_targets(bot_list)[1].tolist()

            # For each item in target_index assign the target via formation[target_index]
            for index in target_index:
                bot = bot_list[target_index.index(index)]
                bot.target = formation[index]

                # Calculate the angles for each point
                bot.target_heading = calculate_degrees(bot.position, bot.target)
                send_msg(f"head#{bot.target_heading}", bot.address)

            formation_assigned = False
            targets_assigned = True

        # If the buffer is empty read any incoming messages
        if len(messages) <= last_message:
            with open("Messages.txt", 'r') as f:
                messages = f.readlines()
        
        # If there are any messages in the buffer that have not been read
        if len(messages) > last_message:
            # Parse incoming message into ('ip-address', port) and messages
            split_message = messages[last_message].strip('\n').split('#')
            
            # Get ip-address and port from message
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
                    if bot is not None:
                        bot.position = pos

                        #When targets are assigned the bots will spam their location so that when they close to their target
                        #The Central Unit can say they need to stop driving
                        if targets_assigned:

                            #Get the distance between the robot and its target
                            distance_to_target = bot.get_distance_to_target()

                            #If the distance is smaller than the error margin allowed
                            if distance_to_target < 0.05:
                                send_msg("stop", bot.address)
                                bot.goal_achieved = True
                    
                    #If there are any ghosts connected to the Central Unit
                    if ghosts_connected:
                        ghost = get_linked_bot(ghost_list, bot)
                        if ghost is not None:
                            send_msg(f"newPos#{bot.position}", ghost.address)


            else:
                #If a robot or the camera tries to connect to the server
                if command == 'wake':
                    #If it is the camera append its IP-Address to the list
                    if name == "camera":
                        address_list.append(address)
                    #If it is a ghost create a GhostBot
                    elif "ghost" in name:  #name should be ghost-[color], matching the bot it simulates
                        ghosts_connected = 1
                        ghost = Ghostbot(address, name, get_bot(bot_list, name.split('-')[1]))
                        ghost_list.append(ghost)
                        address_list.append(address)
                        
                    #And if it's not it is a robot trying to connect
                    #Then create a Robot class
                    else:
                        bot = Robot(address, name)
                        bot_list.append(bot)
                        address_list.append(address)
                    print(f"{command} , {name}")

            # Increment which message has been read last
            last_message += 1

        goals_achieved = 0
        for bot in bot_list:
            if bot.goal_achieved is True:
                goals_achieved += 1

        if goals_achieved == len(bot_list) and goals_achieved > 0:
            print("[INFO] Formation Achieved")
            for bot in bot_list:
                bot.goal_achieved = False
            formation = []
            formation_assigned = False
            targets_assigned = False
            pick_formation = True

        #When program is terminated delete everything in the file
        #And then close it
        if keyboard.is_pressed('q'):
            file = open("Messages.txt", 'w')
            file.truncate()
            file.close()
            break
        
        if keyboard.is_pressed('1') and pick_formation is True:
            formation = formation1
            print("[EXECUTING] Formation 1: Square")
            pick_formation = False
            formation_assigned = True
        if keyboard.is_pressed('2') and pick_formation is True:
            formation = formation2
            print("[EXECUTING] Formation 2: Diamond")
            pick_formation = False
            formation_assigned = True
        if keyboard.is_pressed('3') and pick_formation is True:
            formation = formation3
            print("[EXECUTING] Formation 3: Triangle")
            pick_formation = False
            formation_assigned = True


print("[STARTING] Central Unit")
print("[INFO] To terminate press: q")
start()
