import pygame as pg
pg.init()

screen = pg.display.set_mode((500,500))
pg.display.set_caption('jumping')

player = pg.image.load('Pygame Tutorial/Images/man.png')
player = pg.transform.scale(player, (50,50))
my_rect = player.get_rect(topleft = (200,200))
speed = 5
jump = False
jumpC = 10

clock = pg.time.Clock()

while True:
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
            exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_a] and my_rect.x>0:
        my_rect.x-=speed
    if keys[pg.K_d] and my_rect.x<500- my_rect.width:
        my_rect.x+=speed

    if not jump:
        if keys[pg.K_SPACE]:
            jump = True
    else:
        my_rect.y -= jumpC
        jumpC -=1
        if jumpC < -10:
            jumpC = 10
            jump = False

    screen.fill((110, 200, 36))
    screen.blit(player, my_rect.topleft)
    pg.draw.line(screen,'black', (0, 250), (500, 250), 5)
    pg.display.update()

    clock.tick(40)