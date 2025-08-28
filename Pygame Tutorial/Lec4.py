import pygame
from pygame.locals import *
from sys import exit

screen = pygame.display.set_mode((666, 481), 0, 32,)
background_img = "Images\Tsunami.jpg"
ship = "Images\pirateship.png"


shipimg = pygame.image.load(ship).convert()
x,y = 0,0
move_x, move_y = 0,0

#visit https://pygame.org/docs/ref/key.html for information about keys
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                move_x = -1
            elif event.key == K_RIGHT:
                move_x = +1
            elif event.key == K_UP:
                move_y = -1
            elif event.key == K_DOWN:
                move_y = +1
            
        if event.type == KEYUP:
            if event.key == K_LEFT:
                move_x = 0
            elif event.key == K_RIGHT:
                move_x = 0
            elif event.key == K_UP:
                move_y = 0
            elif event.key == K_DOWN:
                move_y = 0
    x += move_x
    y += move_y
    screen.fill((0,0,0))
    screen.blit(shipimg, (x,y))
    pygame.display.update()