import pygame as pg
pg.init()

screen = pg.display.set_mode((500,500))
pg.display.set_caption('Custom Events')
COLOR = pg.USEREVENT + 1
BOX_GROW = pg.USEREVENT + 2

bg_color = 'white'
grow = True

box = pg.Rect((255,255, 40,40))
screen.fill('white')
clock = pg.time.Clock()

pg.time.set_timer(COLOR, 500)


while True:
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
            exit()
        if events.type == COLOR:
            if bg_color == 'pink':
                screen.fill('pink')
                bg_color = 'white'
            elif bg_color == 'white':
                screen.fill('white')
                bg_color = 'pink'
        if events.type == BOX_GROW:
            if grow:
                box.inflate_ip(4,4)
                grow = box.width <80
            else: 
                box.inflate_ip(-4,-4)
                grow = box.width <40
    if box.collidepoint(pg.mouse.get_pos()):
        pg.event.post(pg.event.Event(BOX_GROW))
    pg.draw.rect(screen,'orange', box)
    pg.display.update()

