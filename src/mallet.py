from __future__ import division
import pygame
from Constant import *


class Mallet:
    pos = [0, 0]
    speed = 0
    ang = 0
    mass = 1
    rad = 0
    img = ''
    draw_pos = [20, 20]
    color = [0, 0, 0]

    def __init__(self, pos, speed, ang, mass, rad, player, color):
        self.pos = pos
        self.speed = speed
        self.ang = ang
        self.mass = mass
        self.rad = rad
        self.player = player
        self.color = color

    def move(self, dt, pos):
        if self.collision_wall(pos):
            return
        # if self.player == 1 and pos[1] <= 0:
        #    pos[1] = +self.rad
        # elif self.player == 2 and pos[1] >= 0:
        #    pos[1] = -self.rad

        self.ang = math.atan2(pos[1] - self.pos[1], pos[0] - self.pos[0]) * 180 / math.pi
        self.speed = math.sqrt((self.pos[1] - pos[1])**2 + (self.pos[0] - pos[0])**2)/(dt*10)
        self.pos = [self.pos[0] + dt *self.speed * math.cos(self.ang/57.2958), self.pos[1] + dt *self.speed * math.sin(self.ang/57.2958)]
        self.draw_pos = scale(self.pos)

    def draw(self, gameDisplay):
        pygame.draw.circle(gameDisplay, self.color, self.draw_pos, self.rad, 4)


    def dist(self, B):
        return math.sqrt((self.pos[0] - B.pos[0])**2 + (self.pos[1] - B.pos[1])**2)

    def move_to(self, pos):
        self.pos = pos
        self.draw_pos = scale(self.pos)

    def collision_wall(self, pos):
        self.ang %= 360
        if pos[1] <= -YMAX_SCALE / 2 or pos[1] >= YMAX_SCALE / 2 or pos[0] <= -XMAX_SCALE / 2 or pos[0] >= XMAX_SCALE / 2:
            return True

        else:
            return False

