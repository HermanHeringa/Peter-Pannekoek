import math

class Robot():
    target = []
    target_heading = 0.0
    address = None
    position = []
    goal_achieved = False

    def __init__(self, color, address):
        self.color = color
        self.address = address

    def get_distance_to_target(self):
        distance = math.sqrt(((self.target[0]-self.position[0])**2)+((self.target[1]-self.position[1])**2))
        print("we zijn dr biiiijjjnaaa")
        return distance