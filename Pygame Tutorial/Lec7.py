# RESIZABLE flag
# pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)

#Windows with no borders

# NOFRAME Flag
# pygame.display.set_mode(SCREEN_SIZE, NOFRAME, 32)

import pygame
from pygame.locals import *
from sys import exit

background_img = "Pygame Tutorial\Images\Tsunami.jpg"
mouse_img = "Pygame Tutorial\Images\pirateship.png"

pygame.init()
SCREEN_SIZE = (640,480)
screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
bgimg = pygame.image.load(background_img).convert()

while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        exit()
    if event.type == VIDEORESIZE:
        SCREEN_SIZE=event.size
        screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
        pygame.display.set_caption("Window resezed to "+str(event.size))
    screen_width , screen_height = SCREEN_SIZE
    for y in range(0,screen_height, bgimg.get_height()):
        for x in range(0,screen_width, bgimg.get_width()):
            screen.blit(bgimg, (x,y))
    pygame.display.update()

# Additional Flags: HWSURFACE (hardware) helps us to make faster bliting
# screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | FULLSCREEN, 32)
# DOUBLEBUF Flag
# screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF | HWSURFACE | FULLSCREEN, 32)