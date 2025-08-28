import pygame as pg
pg.init()

screen = pg.display.set_mode((500,500))
pg.display.set_caption('Designs')

x,y = 100,100
width, height = 10,10
speed = 8





while True:
    pg.time.delay(10)
    for events in pg.event.get():
        if events.type == pg.QUIT:
            exit()
    key = pg.key.get_pressed()

    if key[pg.K_UP] and y>0 :
        y-= speed
    if key[pg.K_DOWN] and y<500-height:
        y+= speed
    if key[pg.K_LEFT] and x>0:
        x-= speed
    if key[pg.K_RIGHT] and x<500-width:
        x += speed

    pg.draw.rect(screen, 'white', (x,y,width,height))
    pg.display.update()