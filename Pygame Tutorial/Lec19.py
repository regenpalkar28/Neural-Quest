import pygame
pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption('Types of Cursors')

system=pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
bitmap = pygame.cursors.Cursor(pygame.cursors.broken_x)

sur = pygame.Surface((10,10))
sur.fill('sky blue')
color = pygame.cursors.Cursor((5,5), sur)

pygame.mouse.set_cursor(system)
clock = pygame.time.Clock()

while True:
    clock.tick(50)
    screen.fill('pink')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_cursor(bitmap)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                pygame.mouse.set_cursor(color)
    pygame.display.flip()
    