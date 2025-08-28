import pygame
pygame.init()
import random

screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('color breezing')
font = pygame.font.SysFont('timesnewroman', 30)

clock = pygame.time.Clock()
c1 = random.randint(0,255)
c2 = random.randint(0,255)
c3 = random.randint(0,255)
RGB = [c1,c2,c3]

def reset():
    global c1, c2, c3
    c1 = random.randint(0,255)
    c2 = random.randint(0,255)
    c3 = random.randint(0,255)
    RGB[0] = c1
    RGB[1] = c2
    RGB[2] = c3

def rgbToHex():
    mapping = {
        10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F'
    }
    converted_hex = [""]*6

    for idx, val in enumerate(RGB):
        hi = val // 16
        lo = val % 16

        converted_hex[2*idx]   = str(mapping[hi] if hi > 9 else hi)
        converted_hex[2*idx+1] = str(mapping[lo] if lo > 9 else lo)

    result = "#" + "".join(map(str, converted_hex))
    return result
    
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            exit()
        if events.type == pygame.MOUSEBUTTONDOWN:
            reset()

    if 0<c1<255:
        c1+=1
    elif c1>255:
        c1 -= 255
    elif c1<=0:
        c1 += 3
    
    clock.tick(500)

    screen.fill((c1,c2,c3))
    hexcode = rgbToHex()
    text_surface = font.render(hexcode, True, (255-c1,255-c2,255-c3))
    screen.blit(text_surface, (20,20))
    pygame.display.update()
