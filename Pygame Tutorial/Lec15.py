import pygame
pygame.init()
from sys import exit
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Moving Object')

x=100
y=100
speed = 3
width = 10
height = 7

while True:
    pygame.time.delay(20)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            exit()
    screen.fill('yellow')
    key = pygame.key.get_pressed()

    if key[pygame.K_a] and x>0:
        x-= speed
    if key[pygame.K_d] and x<500-width:
        x+= speed
    if key[pygame.K_w] and y>0:
        y-= speed
    if key[pygame.K_s] and y<500-height:
        y += speed

    pygame.draw.rect(screen, 'dark green', (x,y,width, height))
    pygame.draw.circle(screen, 'dark green', (x+5, y-5), 5)
    pygame.display.update()