import socket
import pickle
import threading
import cv2
import numpy as np
from Constant import *
import disc as d
import mallet as m
import pygame

cap = cv2.VideoCapture(0)
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((XMAX, YMAX))

font = pygame.font.Font("../fonts/FFF_Tusj.ttf", 60)
bg = pygame.image.load(BG_PATH)

player1 = m.Mallet(PLAYER1_START,MALLET_SPEED,0, MALLET_MASS, 20, 1)
player2 = m.Mallet(PLAYER2_START,MALLET_SPEED,0, MALLET_MASS, 20, 2)

disc = d.Disc(DISC_START_POS,DISC_START_SPEED,DISC_START_ANGLE,DISC_FRICTION,DISC_MASS)
score = [0, 0]

def capture(conn):
    global pos
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
                print(temp)
                threading.Thread(name='send', target=send(conn, temp)).start()


def send(conn, data):
    data = pickle.dumps(data)
    conn.send(data)

def draw(screen):
    screen.blit(bg, scale([-XMAX_SCALE/2 - 28, YMAX_SCALE/2 + 14]))
    disc.draw(screen)
    score1 = font.render(str(score[0]), 1, (255, 255, 255))
    score2 = font.render(str(score[1]), 1, (255, 255, 255))
    screen.blit(score1, scale([-XMAX_SCALE / 4, 0]))
    screen.blit(score2, scale([XMAX_SCALE / 4, 0]))
    player1.draw(screen)
    player2.draw(screen)
    pygame.display.update()


def recv_pos(conn):
    global score
    while True:
        pygame.event.get()
        temp = conn.recv(99).strip()
        clock.tick(250)
        try:
            data = pickle.loads(temp)
            player1.move_to(data[0])
            player2.move_to(data[1])
            disc.move_to(data[2])
            score = data[3]
            threading.Thread(name='draw', target=draw, kwargs=dict(screen=screen)).start()
            pygame.event.pump()

        except:
            continue


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 1234))
    threading.Thread(name='recv', target=recv_pos,kwargs=dict(conn=s)).start()
    return s


#capture(connect())
connect()