# fullscreen

# screen = pygame.display.set_mode((640, 480), 0, 32)

# screen = pygame.display.setmode((640, 480), fullscreen, 32)

import pygame
from pygame.locals import *
from sys import exit

background_img = "Pygame Tutorial\Images\Tsunami.jpg"
mouse_img = "Pygame Tutorial\Images\pirateship.png"

pygame.init()
screen = pygame.display.set_mode((666, 481), 0, 32,)
bgimg = pygame.image.load(background_img).convert()

fullscreen=False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode((1920, 1080), FULLSCREEN, 32,)
            else:
                screen = pygame.display.set_mode((666, 481), 0, 32,)
    screen.blit(bgimg, (0,0))
    pygame.display.update()