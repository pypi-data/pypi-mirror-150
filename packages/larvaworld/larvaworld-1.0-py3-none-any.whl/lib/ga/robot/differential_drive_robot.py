import random

from math import sin, cos, pi



from lib.ga.geometry.rot_triangle import RotTriangle
from lib.ga.util.color import Color


class DifferentialDriveRobot(RotTriangle):

    def __init__(self,  unique_id, model,x, y, length, wheel_radius):
        direction = random.uniform(-pi, pi)
        super().__init__(x, y, length, Color.random_color(127, 127, 127), Color.BLACK, direction)
        self.model = model
        self.unique_id = unique_id
        self.length = length
        self.wheel_radius = wheel_radius
        self.speed_left_wheel = 0.0     # angular velocity of left wheel
        self.speed_right_wheel = 0.0    # angular velocity of left wheel
        self._delta = 0.01
        self.deltax = None
        self.deltay = None

    def step(self):
        """ updates x, y and direction """
        self.delta_x()
        self.delta_y()
        self.delta_direction()

    def move_duration(self, seconds):
        """ Moves the robot for an 's' amount of seconds"""
        for i in range(int(seconds/self._delta)):
            self.step()

    def print_xyd(self):
        """ prints the x,y position and direction """
        print("x = " + str(self.x) +" "+ "y = " + str(self.y))
        print("direction = " + str(self.direction))

    def delta_x(self):
        self.deltax = self._delta * (self.wheel_radius*0.5) * (self.speed_right_wheel + self.speed_left_wheel) * cos(-self.direction)
        self.x += self.deltax

    def delta_y(self):
        self.deltay = self._delta * (self.wheel_radius*0.5) * (self.speed_right_wheel + self.speed_left_wheel) * sin(-self.direction)
        self.y += self.deltay

    def delta_direction(self):
        self.direction += self._delta * (self.wheel_radius/self.length) * (self.speed_right_wheel - self.speed_left_wheel)

        if self.direction > pi:
            self.direction -= 2 * pi
        elif self.direction < -pi:
            self.direction += 2 * pi
