from __future__ import division
import math
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

XMAX_SCALE = 400
YMAX_SCALE = 400
XMAX = 500
YMAX = 760
GOAL_WIDTH = 250
EXTRA_WIDTH = 0.2
MAX_SPEED = 0.8
EXTRA_HIGHT = 0.1

PLAYER1_START = [0, YMAX_SCALE/4]
PLAYER2_START = [0, -YMAX_SCALE/4]

FPS = 60

RESOURCES = '..\\res\\'
BG_PATH = RESOURCES + 'bg.png'
SERVER_SS = RESOURCES + 's_r.jpg'
CLIENT_SS = RESOURCES + 'c_r.jpg'
SS = RESOURCES + 'sbw.png'



#mallet
MALLET_SPEED=0.05
MALLET_FRICTION=0.001
MALLET_MASS=20
MALLET_RAD = 10

#disc
DISC_MAX_SPEED=0.6
DISC_FRICTION=0.0002
DISC_MASS=10
DISC_START_ANGLE=75
DISC_START_POS = [40, 50]
DISC_START_SPEED = 0.05
DISC_RAD = 5




def dist(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def scale_opp(pos, scale):
    return [((pos[0] / scale[0]) * XMAX_SCALE) - (XMAX_SCALE / 2), ((pos[1] / -scale[1]) * YMAX_SCALE) + (YMAX_SCALE / 2)]


def scale(pos):
    draw_pos = [0, 0]
    draw_pos[0] = int((pos[0] + (XMAX_SCALE / 2)) / XMAX_SCALE * XMAX / (EXTRA_WIDTH + 1) + EXTRA_WIDTH / 2 * XMAX)
    draw_pos[1] = int(((((pos[1] - (YMAX_SCALE / 2)) / YMAX_SCALE) * -YMAX) / (EXTRA_HIGHT + 1)) + EXTRA_HIGHT / 2 * YMAX)
    return draw_pos
