import pygame as pg
pg.init()

screen = pg.display.set_mode((500,500))
pg.display.set_caption('Circle Animation')

x,y = 200,200
xv = 5
yv = -5

clock = pg.time.Clock()
while True:
    screen.fill('sky blue')
    pg.draw.circle(screen, 'orange', (x,y), 10)
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
    x += xv
    y += yv 
    if x>490 or x<10:
        xv *= -1
    if y>490 or y<10:
        yv *= -1
    pg.display.update()
    clock.tick(50)