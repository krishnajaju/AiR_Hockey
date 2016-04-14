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


score = [0, 0]
cap = cv2.VideoCapture(0)
pygame.init()
screen = pygame.display.set_mode((XMAX, YMAX))
#load images
bg = pygame.image.load(BG_PATH)

player1 = Mallet(PLAYER1_START,MALLET_SPEED,0, MALLET_MASS, 15, 1)
player2 = Mallet(PLAYER2_START,MALLET_SPEED,0, MALLET_MASS, 15, 2)
disc = d.Disc(DISC_START_POS,DISC_START_SPEED,DISC_START_ANGLE, DISC_FRICTION,DISC_MASS)
font = pygame.font.Font("../fonts/FFF_Tusj.ttf", 60)

clock = pygame.time.Clock()
score1 = score2 = font.render(str(score[0]), 1, (255, 255, 255))



player2_pos = PLAYER2_START

player1_pos = PLAYER1_START

def capture():
    global player1_pos
    h = w = 0
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
                player1_pos = temp


def draw(screen):
    global score1, score2
    # draw
    screen.fill((0, 0, 0))
    screen.blit(bg, scale([-XMAX_SCALE/2 - 30, YMAX_SCALE/2 + 14]))
    screen.blit(score1, scale([-XMAX_SCALE/4, 0]))
    screen.blit(score2, scale([XMAX_SCALE/4, 0]))
    player1.draw(screen)
    player2.draw(screen)
    disc.draw(screen)

    # draw goals
    pygame.draw.line(screen, (0, 0, 255), scale([- XMAX_SCALE / 2 + GOAL_WIDTH / 2, YMAX_SCALE / 2]),
                     scale([XMAX_SCALE / 2 - GOAL_WIDTH / 2, YMAX_SCALE / 2]))
    pygame.draw.line(screen, (0, 0, 255), scale([- XMAX_SCALE / 2 + GOAL_WIDTH / 2, YMAX_SCALE / 2 + disc.rad]),
                     scale([XMAX_SCALE / 2 - GOAL_WIDTH / 2, YMAX_SCALE / 2 + disc.rad]))
    pygame.draw.line(screen, (0, 0, 255), scale([- XMAX_SCALE / 2 + GOAL_WIDTH / 2, -YMAX_SCALE / 2]),
                     scale([XMAX_SCALE / 2 - GOAL_WIDTH / 2, -YMAX_SCALE / 2]))
    pygame.draw.line(screen, (0, 0, 255), scale([- XMAX_SCALE / 2 + GOAL_WIDTH / 2, -YMAX_SCALE / 2 - disc.rad]),
                     scale([XMAX_SCALE / 2 - GOAL_WIDTH / 2, -YMAX_SCALE / 2 - disc.rad]))
    # lines
    pygame.draw.line(screen, (0, 255, 255), scale([- XMAX_SCALE / 2, YMAX_SCALE / 2]),
                     scale([XMAX_SCALE / 2, YMAX_SCALE / 2]))
    pygame.draw.line(screen, (0, 255, 255), scale([- XMAX_SCALE / 2, YMAX_SCALE / 2]),
                     scale([-XMAX_SCALE / 2, -YMAX_SCALE / 2]))
    pygame.draw.line(screen, (0, 255, 255), scale([- XMAX_SCALE / 2, -YMAX_SCALE / 2]),
                     scale([XMAX_SCALE / 2, -YMAX_SCALE / 2]))
    pygame.draw.line(screen, (0, 255, 255), scale([XMAX_SCALE / 2, YMAX_SCALE / 2]),
                     scale([XMAX_SCALE / 2, -YMAX_SCALE / 2]))
    pygame.display.update()


def start(conn):
    #threads are started
    threading.Thread(name='Threaded camera', target=capture).start()
    threading.Thread(name='recv', target=recv_pos, kwargs=dict(conn=conn)).start()

    global player2_pos, player1_pos, score, score1, score2
    #main game loop
    while True:
        pygame.event.get()
        dt = clock.tick(500)
        #score addition
        goal = disc.collision_wall()
        if goal == 2:
            score[0] += 1
            score1 = font.render(str(score[0]), 1, (255, 255, 255))
        elif goal == 3:
            score[1] += 1
            score2 = font.render(str(score[1]), 1, (255, 255, 255))

        goal = disc.collision(player1)
        if goal == 2:
            score[0] += 1
            score1 = font.render(str(score[0]), 1, (255, 255, 255))
        elif goal == 3:
            score[1] += 1
            score2 = font.render(str(score[1]), 1, (255, 255, 255))

        goal = disc.collision(player2)
        if goal == 2:
            score[0] += 1
            score1 = font.render(str(score[0]), 1, (255, 255, 255))
        elif goal == 3:
            score[1] += 1
            score2 = font.render(str(score[1]), 1, (255, 255, 255))

        player1.move(dt, player1_pos)
        player2.move(dt, player2_pos)
        disc.move(dt)
        threading.Thread(name='draw', target=draw, kwargs=dict(screen=screen)).start()
        threading.Thread(name='send', target=send_pos, kwargs=dict(conn=conn)).start()
    pygame.quit()
    quit()


def send_pos(conn):
    global score
    data = [player1.pos, player2.pos, disc.pos, score]
    data = pickles.dumps(data, -1)
    try:
        conn.send(data)
    except:
        #failed  to send
        exit()
    return


def recv_pos(conn):
    global player2_pos
    while True:
        data = conn.recv(1024)
        player2_pos = [pickle.loads(data)[0], pickle.loads(data)[1]]


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 1234))
    s.listen(1)
    conn, addr = s.accept()
    return conn

start(connect())
#start(0)

