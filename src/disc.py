from __future__ import division
import pygame
from Constant import *

class Disc:
    pos = [0, 0]
    speed = 0
    ang = 0
    friction = 0
    mass = 1
    rad = 10
    color = [0, 0, 0]
    draw_pos = [0, 0]

    def __init__(self, pos, speed, ang, friction, mass, rad, color):
        self.pos = pos
        self.speed = speed
        self.ang = ang
        self.friction = friction
        self.mass = mass
        self.rad = rad
        self.color = color

    def move(self, dt):
        if self.speed <= 0:
            self.speed = 0
        else:
            self.speed = self.speed - self.friction * dt
        self.pos[0] += dt * math.cos(self.ang / 57.2958) * self.speed
        self.pos[1] += dt * math.sin(self.ang / 57.2958) * self.speed
        # replace with the image
        self.draw_pos = scale(self.pos)

    def move_to(self, pos):
        self.pos = pos
        self.draw_pos = scale(self.pos)

    def draw(self, gameDisplay):
        pygame.draw.circle(gameDisplay, self.color, self.draw_pos, self.rad, 0)

    def collision(self, B):
        if self.rad + self.pos[0] + B.rad > B.pos[0] and self.pos[0] < self.rad + B.rad + B.pos[0] and \
                                        self.rad + self.pos[1] + B.rad > B.pos[1] and self.pos[1] < self.rad + B.rad + \
                B.pos[1]:
            if dist(self.pos, B.pos) <= B.rad + self.rad:
                newVelX1 = (math.cos(self.ang / 57.2958) * self.speed * (self.mass - B.mass) + (
                2 * B.mass * B.speed * math.cos(B.ang / 57.2958))) / (self.mass + B.mass)
                newVelY1 = (math.sin(self.ang / 57.2958) * self.speed * (self.mass - B.mass) + (
                2 * B.mass * B.speed * math.sin(B.ang / 57.2958))) / (self.mass + B.mass)

                self.ang = math.atan2(newVelY1, newVelX1) * 57.2958
                self.speed = math.sqrt(newVelY1 ** 2 + newVelX1 ** 2)
                if self.speed > MAX_SPEED:
                    self.speed = MAX_SPEED
                while dist(self.pos, B.pos) <= B.rad + self.rad and dist([self.pos[0] + newVelX1, self.pos[1] + newVelY1], B.pos) > dist(self.pos, B.pos):
                    goal = self.collision_wall()
                    if goal != 0:
                        self.speed = 0
                        return goal
                    self.pos[0] += newVelX1
                    self.pos[1] += newVelY1
        return 0

    def collision_wall(self):
        self.ang %= 360
        if self.pos[1] <= -YMAX_SCALE / 2:
            # bottom wall
            if - XMAX_SCALE / 2 + GOAL_WIDTH/2 < self.pos[0] < XMAX_SCALE / 2 - GOAL_WIDTH/2:
                if self.pos[1] <= -YMAX_SCALE/2 - self.rad:
                    self.pos = [-XMAX_SCALE/2, 0] #bottom goal
                    self.speed = 0.15
                    self.ang = 330
                    return 3
                else:
                    return 0
            if 180 < self.ang:
                self.ang = -self.ang
            elif self.ang == 180 or self.ang == 0:
                self.ang = 90
        elif self.pos[1] >= YMAX_SCALE / 2:
            # top wall
            if - XMAX_SCALE / 2 + GOAL_WIDTH/2 < self.pos[0] < XMAX_SCALE / 2 - GOAL_WIDTH/2:
                if self.pos[1] >= YMAX_SCALE/2 + self.rad:
                    self.pos = [-XMAX_SCALE/2, 0] #top goal
                    self.speed = 0.15
                    self.ang = 30
                    return 2
                else:
                    return 0
            if self.ang < 180:
                self.ang = -self.ang
            elif self.ang == 180 or self.ang == 0:
                self.ang = 270
        elif self.pos[0] <= -XMAX_SCALE / 2:
            # left wall
            if 90 < self.ang < 270:
                self.ang = 180 - self.ang
            elif self.ang == 270 or self.ang == 90:
                self.ang = 180
        elif self.pos[0] >= XMAX_SCALE / 2:
            # right wall
            if 270 < self.ang or self.ang < 90:
                self.ang = 180 - self.ang
            elif self.ang == 270 or self.ang == 90:
                self.ang = 180
        else:
            return 0
        return 1
