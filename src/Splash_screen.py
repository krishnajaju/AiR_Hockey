import pygame
from Constant import *

def server():
    print('server')

def client():
    print(client)


pygame.init()
screen = pygame.display.set_mode((100, 100))
s = pygame.image.load(SERVER_SS)
c = pygame.image.load(CLIENT_SS)
bg = pygame.image.load(BG_PATH)

while True:
    pygame.event.get()

    pos = pygame.mouse.get_pos()

    if pos[0] > 50:
        print('RIGHT')
    else:
        print ('left')