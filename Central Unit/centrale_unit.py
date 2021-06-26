from scipy.optimize import linear_sum_assignment
import math
import socket
import numpy as np
import keyboard
from Robot import Robot
from GhostBot import Ghostbot

UDP_IP = "127.0.0.1"
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


def get_targets(bot_list):
    distances = []
    for bot in bot_list:
        distances.append(bot.distance_to_targets)
    
    cost = np.array(distances)

    return linear_sum_assignment(cost)


def calculate_degrees(position, target):
    deltaX = target[0] - position[0]
    deltaY = target[1] - position[1]
    return -round(float(np.degrees(np.math.atan2(deltaY, deltaX))))  # Casting to float first seems redundant, but IDE throws a warning if you don't


def send_msg(message, address):
    print(f"[SENDING] Message: {message} to address {address}")
    sock.sendto(str(message).encode(), address)


def get_bot(bot_list, name):
    for _bot in bot_list:
        if _bot.name == name:
            return _bot


def get_linked_bot(ghost_list, linked_bot):
    for _ghost in ghost_list:
        print(_ghost)
        print(linked_bot)
        print(_ghost.linked_bot)
        print("hfsdjahgjsdljkghksdj")
        if _ghost.linked_bot == linked_bot:
            print(type(_ghost))
            print("AAAA")
            return _ghost
    

def start():
    field_width = 1.92
    field_height = 1.08
    side_margin = 0.2

    messages = []
    bot_list = []
    address_list = []

    ghosts_connected = 0
    ghost_list = []

    formation = []
    formation1 = [[side_margin, side_margin],
                  [field_width - side_margin, side_margin],
                  [side_margin, field_height - side_margin],
                  [field_width - side_margin, field_height - side_margin]]
    formation2 = [[field_width/2, side_margin],
                  [side_margin, field_height/2],
                  [field_width/2, field_height-side_margin],
                  [field_width-side_margin, field_height/2]]
    formation3 = [[side_margin, side_margin], 
                  [field_width/2, side_margin],
                  [field_width-side_margin, side_margin],
                  [field_width/2, field_height-side_margin]]

    pick_formation = True
    formation_assigned = True
    targets_assigned = False
    # Counter for last message that is read
    last_message = 0

    while True:
        if bot_list != [] and formation != [] and pick_formation is False and formation_assigned is True:
            # For all the robots in the list check which distance is closest and set that as a target
            calculate_distances(formation, bot_list)

            target_index = get_targets(bot_list)[1].tolist()

            # For each item in target_index assign the target via formation[target_index]
            for index in target_index:
                bot = bot_list[target_index.index(index)]
                bot.target = formation[index]
                # bot0: 0 bot1: 2 bot3: 1 bot4:3

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
            
            # If the address isn't in the list add it to the list
            if address in address_list:
                
                # Handle incoming commands here that are not 'wake' because the bots are already added
                if command == "pos":
                    data = split_message[3]
                    data = data.strip('\'[]\'').split(', ')
                    pos = [float(data[0]), float(data[1])]
                    
                    bot = get_bot(bot_list, name)
                    if bot is not None:
                        bot.position = pos

                        # When targets are assigned the bots will spam their location so that when they close to their target
                        # The Central Unit can say they need to stop driving
                        if targets_assigned:
                            # Check if the position has been reached with a margin of error
                            # This will be harder than expected
                            # You need to track again if the target is left/right behind/front

                            # For all targets that every robot is assigned to
                            distance_to_target = bot.get_distance_to_target()
                            print(distance_to_target)
                            if distance_to_target < 0.05:
                                send_msg("stop", bot.address)
                                bot.goal_achieved = True

                    if ghosts_connected:
                        ghost = get_linked_bot(ghost_list, bot)
                        if ghost is not None:
                            send_msg(f"newPos#{bot.position}", ghost.address)

            else:
                print("ree")
                if command == 'wake':
                    if name == "camera":
                        address_list.append(address)
                    elif "ghost" in name:  # name should be ghost-[color], matching the bot it simulates
                        print(address)
                        ghosts_connected = 1
                        ghost = Ghostbot(address, name, get_bot(bot_list, name.split('-')[1]))
                        print(ghost)
                        ghost_list.append(ghost)
                        address_list.append(address)
                        
                    
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

        # When program is terminated delete everything in the file
        # And then close it
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
