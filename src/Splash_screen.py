import pygame
from Constant import *
import Client_options
import Server_options

def server():
    print('server')

def client():
    print(client)


pygame.init()
screen = pygame.display.set_mode((670, 335))
s = pygame.image.load(SERVER_SS)
c = pygame.image.load(CLIENT_SS)
bg = pygame.image.load(SS)
font_main = pygame.font.Font("../fonts/Merkur.otf", 70)
main_text = font_main.render('AiR HOCKEY', 1, (50, 202, 50))
font_option = pygame.font.Font("../fonts/FFF_Tusj.ttf", 40)
server_text = font_option.render('Server', 1, white)
client_text = font_option.render('Client', 1, white)

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pygame.quit()
            if pos[0] > 335:
                Client_options.start()
            else:
                Server_options.start()
            exit()
    screen.fill(black)
    screen.blit(bg, (0, 0))
    if pos[0] > 335:
        screen.blit(c, (338, 0))
        screen.blit(client_text, (550, 50))
    else:
        screen.blit(s, (0, 00))
        screen.blit(server_text, (10, 50))

    screen.blit(main_text, (190, 0))
    pygame.display.update()
