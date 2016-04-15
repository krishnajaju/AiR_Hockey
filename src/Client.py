from mallet import *
import pygame
import socket
import disc as d
import cv2
import numpy as np
import pygame
import threading
import cPickle as pickles
from Constant import *
import pickle

screen_c = 0
bg = pygame.image.load(BG_PATH)
score = [0, 0]
player1 = player2 = disc = score1 = score2 = 0
clock = pygame.time.Clock()
pygame.init()
screen_c = pygame.display.set_mode((XMAX, YMAX))

player2_pos = PLAYER2_START
player1_pos = PLAYER1_START
PLAYER1_COLOR = [255, 0, 0]
PLAYER2_COLOR = [255, 0, 0]
PUCK_COLOR = [255, 0, 0]
MAX_TIME = -1
MAX_GOAL = -1

def init():
    global player2, player1, disc, score1, score2, clock, player2_pos, player1_pos, score, screen_c

    player1 = Mallet(PLAYER1_START, MALLET_SPEED, 0, MALLET_MASS, 15, 1, PLAYER1_COLOR)
    player2 = Mallet(PLAYER2_START, MALLET_SPEED, 0, MALLET_MASS, 15, 2, PLAYER2_COLOR)
    disc = d.Disc(DISC_START_POS, DISC_START_SPEED, DISC_START_ANGLE, DISC_FRICTION, DISC_MASS, PUCK_COLOR)
    score1 = score2 = 0
    clock = pygame.time.Clock()
    player2_pos = PLAYER2_START
    player1_pos = PLAYER1_START
    score = [0, 0]

def capture(conn):
    global pos
    h = w = 0
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        # hue saturation value
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if h == 0:
            (w, h) = hsv.shape[:2]
        cv2.flip(hsv, 1, hsv)
        lower_pink = np.array([10, 150, 0])
        upper_pink = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_pink, upper_pink)
        kernal = np.ones((15, 15), np.float32) / 225
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
        cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 10:
                temp = scale_opp([int(x), int(y)], [h, w])
                threading.Thread(name='send', target=send(conn, temp)).start()

def send(conn, data):
    data = pickle.dumps(data)
    conn.send(data)

def draw(font):
    screen_c.fill((0, 0, 0))
    screen_c.blit(bg, scale([-XMAX_SCALE/2 - 28, YMAX_SCALE/2 + 14]))
    disc.draw(screen_c)
    score1 = font.render(str(score[0]), 1, (255, 255, 255))
    score2 = font.render(str(score[1]), 1, (255, 255, 255))
    screen_c.blit(score1, scale([-XMAX_SCALE / 4, 0]))
    screen_c.blit(score2, scale([XMAX_SCALE / 4, 0]))
    player1.draw(screen_c)
    player2.draw(screen_c)
    pygame.display.update()


def recv_pos(conn):
    global score, screen_c
    font = pygame.font.Font("../fonts/scoreboard.ttf", 60)
    while True:
        # Events
        pygame.event.get()
        try:
            temp = conn.recv(99).strip()
            data = pickle.loads(temp)
            player1.move_to(data[0])
            player2.move_to(data[1])
            disc.move_to(data[2])
            score = data[3]
            threading.Thread(name='draw', target=draw, kwargs=dict(font=font)).start()
        except Exception as e:
            continue
    pygame.quit()
    quit()

def connect(ip):
    print(ip)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.121', 1234))
    return s

def start(s):
    threading.Thread(name='recv', target=recv_pos,kwargs=dict(conn=s)).start()
    capture(s)

def main(ip):
    global PLAYER1_COLOR, PLAYER2_COLOR, MAX_GOAL, MAX_TIME, PUCK_COLOR, screen_c
    conn = connect(ip)
    list = pickle.loads(conn.recv(1024))
    MAX_TIME = int(list[0])
    MAX_GOAL = int(list[1])
    PLAYER1_COLOR = list[2:5]
    PUCK_COLOR = list[5:8]
    PLAYER1_COLOR = [int(word) for word in PLAYER1_COLOR]
    PUCK_COLOR = [int(word) for word in PUCK_COLOR]
    file = open('settings_c.txt', 'r')
    PLAYER2_COLOR = [int(word.strip()) for word in file.readlines()]
    conn.send(pickle.dumps(PLAYER2_COLOR))
    #todo loop here is needed
    init()
    threading.Thread(name='draw', target=start, kwargs=dict(s=conn)).start()

