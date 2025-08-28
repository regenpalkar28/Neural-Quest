import pygame
from sys import exit
pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Scaling')
image = pygame.image.load('Pygame Tutorial\Images\Tsunami.jpg')
image = pygame.transform.scale(image, (400,400))

while True:
    screen.fill('white')
    screen.blit(image,(0,0))
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            exit()
    pygame.display.update()