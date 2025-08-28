import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((400,400))
snow = []

#splash and its variables
splash_path = pygame.image.load('Pygame Tutorial\Images\Splash.png')
splash_duration = 300


for i in range(70):
    x = random.randint(0,400)
    y = random.randint(0,400)
    speed = random.randint(2,5)
    snow.append([x,y,speed,None])

clock = pygame.time.Clock()

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            exit()
    screen.fill('white')

    for ice in snow:
        if not ice[3]:
            ice[1]+=ice[2]

        if ice[1] >= 400 and not ice[3]:
            # When raindrop reaches the bottom, splash is to be started
            ice[3] = pygame.time.get_ticks()
            ice[1] = 400
        pygame.draw.circle(screen, 'sky blue',ice[:2], 3)

        if ice[3]:
            if pygame.time.get_ticks() - ice[3] < splash_duration:
                splash_rect = splash_path.get_rect(center=(ice[0], ice[1]-20))
                screen.blit(splash_path, splash_rect)
            else:
                # Reset drop after splash
                ice[1] = random.randrange(-50, -10)
                ice[0] = random.randrange(0,400)
                ice[3] = None
    pygame.display.update()
    clock.tick(40)
