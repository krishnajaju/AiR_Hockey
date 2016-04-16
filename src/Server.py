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
from Chrono import Chrono
bg = pygame.image.load(BG_PATH)
score = [0, 0]
score1 = score2 = 0

clock = pygame.time.Clock()

player2_pos = PLAYER2_START
player1_pos = PLAYER1_START
PLAYER1_COLOR = red
PLAYER2_COLOR = blue
PUCK_COLOR = green
MAX_TIME = -1
MAX_GOAL = -1


#load images
def init():
    global player2, player1, disc, score1, score2, clock, player2_pos, player1_pos, score, chrono, font, font_small
    chrono = Chrono(0, 0, 0)
    font = pygame.font.Font("../fonts/scoreboard.ttf", 60)
    font_small = pygame.font.Font("../fonts/scoreboard.ttf", 30)
    disc.pos = [0, 0]
    score = [0, 0]
    score1 = score2 = 0
    clock = pygame.time.Clock()
    player1_pos = PLAYER1_START
    player2_pos = PLAYER2_START
    player1.pos = player1_pos
    player2.pos = player2_pos
    score1 = font.render(str(score[0]), 1, white)
    score2 = font.render(str(score[1]), 1, white)
    draw(screen=screen)


def capture():
    global player1_pos
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
                player1_pos = temp


def draw(screen):
    global score1, score2, font, font_small
    # draw
    screen.fill(black)
    screen.blit(bg, scale([-XMAX_SCALE/2 - 30, YMAX_SCALE/2 + 14]))
    screen.blit(score1, scale([-XMAX_SCALE/4 - XMAX_SCALE/16, -YMAX_SCALE/26]))
    screen.blit(score2, scale([XMAX_SCALE/4, YMAX_SCALE/8]))
    time = font_small.render(chrono.__str__(), 1, white)
    screen.blit(time, scale([-XMAX_SCALE/12, YMAX_SCALE/46]))
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
    global player2_pos, player1_pos, score, score1, score2, font
    score1 = score2 = font.render(str(score[0]), 1, white)
    threading.Thread(name='Threaded camera', target=capture).start()
    threading.Thread(name='recv', target=recv_pos, kwargs=dict(conn=conn)).start()

    #main game loop
    while True:
        pygame.event.get()
        dt = clock.tick(500)
        chrono.add_millisecond(dt)

        player1.move(dt, player1_pos)
        player2.move(dt, player2_pos)

        if (score[0] == MAX_GOAL or score[1] == MAX_GOAL) or (MAX_TIME != -1 and chrono.get_minute() >= MAX_TIME and score[0] != score[1]):
            winner = end_game()
            send_pos(conn, winner)
            break

        #score addition
        goal = disc.collision_wall()
        if goal == 2:
            score[0] += 1
            score1 = font.render(str(score[0]), 1, white)
        elif goal == 3:
            score[1] += 1
            score2 = font.render(str(score[1]), 1, white)

        goal = disc.collision(player1)
        if goal == 2:
            score[0] += 1
            score1 = font.render(str(score[0]), 1, white)
        elif goal == 3:
            score[1] += 1
            score2 = font.render(str(score[1]), 1, white)

        goal = disc.collision(player2)
        if goal == 2:
            score[0] += 1
            score1 = font.render(str(score[0]), 1, white)
        elif goal == 3:
            score[1] += 1
            score2 = font.render(str(score[1]), 1, white)

        disc.move(dt)
        threading.Thread(name='draw', target=draw, kwargs=dict(screen=screen)).start()
        threading.Thread(name='send', target=send_pos, kwargs=dict(conn=conn)).start()

def end_game():
    # opposite scores ##top score 1 ##bottom score2
    if score[0] > score[1]:
        winner = 0
        end_label = font.render("PLAYER 1 WINS!", 1, PLAYER1_COLOR)
    else:
        winner = 1
        end_label = font.render("PLAYER 2 WINS!", 1, PLAYER2_COLOR)

    screen.blit(end_label,(XMAX*0.5-end_label.get_width()*0.5,YMAX*0.5))
    pygame.display.update()
    pygame.time.wait(3000)
    clock.tick(500)
    return winner


def send_pos(conn, winner=-1):
    global score
    data = [player1.pos, player2.pos, disc.pos, score, chrono.__str__(), winner]
    data = pickles.dumps(data, -1)
    try:
        conn.send(data)
    except:
        exit()
    return


def recv_pos(conn):
    global player2_pos
    while True:
        data = conn.recv(1024)
        player2_pos = [pickle.loads(data)[0], pickle.loads(data)[1]]


def connect(list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 1234))
    s.listen(1)
    conn, addr = s.accept()
    conn.send(pickle.dumps(list))
    return conn

def main():
    #reading full settings
    global PLAYER1_COLOR, PLAYER2_COLOR, MAX_GOAL, MAX_TIME, PUCK_COLOR, screen,player1, player2,disc
    file = open('settings_s.txt', 'r')
    list = [word.strip() for word in file.readlines()]
    MAX_TIME = int(list[0])
    MAX_GOAL = int(list[1])
    PLAYER1_COLOR = list[2:5]
    PUCK_COLOR = list[5:8]
    PLAYER1_COLOR = [int(word) for word in PLAYER1_COLOR]
    PUCK_COLOR = [int(word) for word in PUCK_COLOR]
    conn = connect(list)
    #todo recv client color
    PLAYER2_COLOR = [int(word) for word in pickle.loads(conn.recv(1024))]
    pygame.init()
    screen = pygame.display.set_mode((XMAX, YMAX))
    player1 = Mallet(PLAYER1_START, MALLET_SPEED, 0, MALLET_MASS, MALLET_RAD, 1, PLAYER1_COLOR)
    player2 = Mallet(PLAYER2_START, MALLET_SPEED, 0, MALLET_MASS, MALLET_RAD, 2, PLAYER2_COLOR)
    disc = d.Disc(DISC_START_POS, DISC_START_SPEED, DISC_START_ANGLE, DISC_FRICTION, DISC_MASS, DISC_RAD, PUCK_COLOR)

    #todo possable loop for multiple games
    while(True):
        init()
        start(conn)
    pygame.quit()
    quit()


