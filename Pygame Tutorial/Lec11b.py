import pygame
from sys import exit
pygame.init()
win = pygame.display.set_mode((500,500))
Font = pygame.font.SysFont('timesnewroman', 30)
letter = Font.render('Pygame', False, 'orange')
i=0
while True:
    if i>500:
        i=0
        pygame.time.wait(30)
    
    win.fill('white')
    win.blit(letter,(0,i))
    i += 10

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
    pygame.time.wait(30)
    