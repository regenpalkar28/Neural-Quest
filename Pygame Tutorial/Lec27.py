import pygame as pg
pg.init()

screen = pg.display.set_mode((500,500))
pg.display.set_caption("Text!")

text = "Hello Everyone! \nWe are trying to display text on pygame window blah blah blah blah blah blah blah blah and a bunch of blahs"
font = pg.font.SysFont('timesnewroman', 30)


def display_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0] # 0 is width, 1 is height
    x,y = pos
    max_width = surface.get_width()
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height

while True:
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill((45, 54, 176))
    display_text(screen, text, (20,20), font, 'purple')
    pg.display.update()