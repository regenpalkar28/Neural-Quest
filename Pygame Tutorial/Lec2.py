import pygame
from pygame.locals import *
from sys import exit

background_img = "Pygame Tutorial\Images\Tsunami.jpg"
mouse_img = "Pygame Tutorial\Images\pirateship.png"

pygame.init()

screen = pygame.display.set_mode((666, 481), 0, 32,)
pygame.display.set_caption("Ship battling the currents")
bgimg = pygame.image.load(background_img).convert()
mouse = pygame.image.load(mouse_img).convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
    # blit takes the background image and a tuple containing destination posn 
    screen.blit(bgimg, (0,0))
    x,y = pygame.mouse.get_pos()
    # x and y is coordinates of mouse pointer
    x -= mouse.get_width()/2
    y -= mouse.get_height()/2
    # centers the cursor to center of image
    screen.blit(mouse, (x,y))
    pygame.display.update()
#this helps us to show image from memory to user without flicker