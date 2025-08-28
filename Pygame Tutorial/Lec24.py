import pygame as pg
import math
pg.init()
screen = pg.display.set_mode((1000, 500))

while True:
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
    t = (pg.time.get_ticks()/3)%1000
    x = t
    y = math.sin(t/50)*100 + 200
    screen.fill('sky blue')
    pg.draw.circle(screen, 'orange', (x,y), 10)
    pg.display.update()