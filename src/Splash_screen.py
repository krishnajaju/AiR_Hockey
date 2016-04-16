import pygame
from Constant import *

def server():
    print('server')

def client():
    print(client)


pygame.init()
screen = pygame.display.set_mode((700, 500))
s = pygame.image.load(SERVER_SS)
c = pygame.image.load(CLIENT_SS)
bg = pygame.image.load(SS)
#font_main =
while True:
    pygame.event.get()
    screen.fill(black)
    screen.blit(bg, (0, 0))
    pos = pygame.mouse.get_pos()
    if pos[0] > 350 and pos[1] > 0:
        screen.blit(c, (338, 0))
    elif pos[1] > 50:
        screen.blit(s, (0, 0))
    pygame.display.update()
