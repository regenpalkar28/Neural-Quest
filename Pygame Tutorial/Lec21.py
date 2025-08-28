import pygame as pg
pg.init()

screen = pg.display.set_mode((500,500))
pg.display.set_caption('User Input')


user_ip = ""
font = pg.font.SysFont('timesnewroman', 30)
text_box = pg.Rect(75,75,100,50)
active = False
color = pg.Color('purple')

while True:
    for events in pg.event.get():
        if events.type == pg.QUIT:
            exit()
        if events.type == pg.MOUSEBUTTONDOWN:
            if text_box.collidepoint(events.pos):
                active = True
            else:
                active = False
        if events.type == pg.KEYDOWN:
            if active:
                if events.key == pg.K_BACKSPACE:
                    user_ip = user_ip[:-1]
                else:
                    user_ip += events.unicode
    screen.fill('sky blue')

    if active:
        color = pg.Color(156, 167, 184)
    else:
        color = pg.Color(94, 101, 112)
    pg.draw.rect(screen, color, text_box,4)
    surf = font.render(user_ip, True, 'orange')
    screen.blit(surf, (text_box.x +5, text_box.y +5))
    text_box.w = max(100, surf.get_width()+10)
    pg.display.update()