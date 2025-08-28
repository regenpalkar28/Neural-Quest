import pygame as pg
pg.init()
import random
import time
screen = pg.display.set_mode((500,500))
pg.display.set_caption('Collision')

clock = pg.time.Clock()
speed = 5
font = pg.font.SysFont('timesnewroman', 50)

class Brick(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Pygame Tutorial/Images/brick.png')
        self.image = pg.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 300-40), 0)

    def motion(self):
        self.rect.move_ip(0,speed)
        if self.rect.top > 500:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 470), 0)

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Pygame Tutorial/Images/man.png')
        self.image = pg.transform.scale(self.image, (100,150))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 420)

    def motion(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.move_ip(-5, 0) 
        if keys[pg.K_d]:
            self.rect.move_ip(5, 0)

M1 = Player()
B1 = Brick()

bricks = pg.sprite.Group()
bricks.add(B1)

all_sprites = pg.sprite.Group()
all_sprites.add(M1)
all_sprites.add(B1)


while True:
    screen.fill('white')
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.motion()

    if pg.sprite.spritecollideany(M1, bricks):
        text = font.render('Game Over', True, 'orange')
        text_rect = text.get_rect(center=(500//2,500//2))
        screen.blit(text, text_rect)
        time.sleep(2)

    pg.display.flip()
    clock.tick(40)