import math

class Robot:
    name = ""
    target = []
    target_heading = 0.0
    distance_to_targets = []
    address = None
    position = []
    goal_achieved = False

    def __init__(self, address, name):
        self.address = address
        self.name = name
        print(name)

    #Function to calculate the distance between the robot and it's assigned target
    #Using the pythagorean theorem
    def get_distance_to_target(self):
        distance = math.sqrt(((self.target[0]-self.position[0])**2)+((self.target[1]-self.position[1])**2))
        return distance
