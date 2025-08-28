import pygame
pygame.init()
from sys import exit
screen = pygame.display.set_mode((600,600))
ball = pygame.image.load(r"Pygame Tutorial\Images\pirateship.png").convert()
ballrect = ball.get_rect()
speed = [10,0]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > 600:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > 600:
        speed[1] = -speed[1]

    screen.fill((255,255,255))
    screen.blit(ball, ballrect)
    pygame.display.flip()

