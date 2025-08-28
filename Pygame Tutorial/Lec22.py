import pygame as pg
from sys import exit
pg.init()
screen = pg.display.set_mode((500,500))
pg.display.set_caption('Testing Buttons')

font = pg.font.SysFont('timesnewroman', 40, bold=True)
surf = font.render('QUIT', True, 'white')
button = pg.Rect(200,200,110,60)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                pg.quit()
                exit()

    a,b = pg.mouse.get_pos()

    if button.x <= a <= button.x+110 and button.y <= b <= button.y + 60:
        pg.draw.rect(screen, (180,180,180), button)
    else:
        pg.draw.rect(screen, (110,110,110), button)
    screen.blit(surf, (button.x+5, button.y+5))

    pg.display.update()