import pygame
pygame.init()
from sys import exit
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption('Snake')

import time
import random

snake_head = [80,30]
snake_speed = 10

clock = pygame.time.Clock()

snake_body = [[80,30], [70,30]]

food_pos = [random.randrange(1,(600//10))*10, random.randrange(1,(500//10))*10]
food = True

score = 0

def show_score():
    font = pygame.font.SysFont('Georgia', 30)
    Font = font.render('Score: '+str(score), True, 'pink')
    rect = Font.get_rect()
    screen.blit(Font,rect)

def game_over():
    font = pygame.font.SysFont('Georgia', 30)
    Font = font.render(
        'GAME OVER Score: ' + str(score), True, 'purple')
    rect = Font.get_rect
    rect.midtop = (600/2, 500/4)
    screen.blit(Font,rect)
    pygame.display.flip()
    time.sleep(2)   
    exit()

dir = 'RIGHT'
next_dir = dir

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                next_dir = 'UP'
            if event.key == pygame.K_s:
                next_dir = 'DOWN'
            if event.key == pygame.K_a:
                next_dir = 'LEFT'
            if event.key == pygame.K_d:
                next_dir = 'RIGHT'
        
    if next_dir == 'UP' and dir != 'DOWN':
        dir = 'UP'
    if next_dir == 'DOWN' and dir != 'UP':
        dir = 'DOWN'
    if next_dir == 'LEFT' and dir != 'RIGHT':
        dir = 'LEFT'
    if next_dir == 'RIGHT' and dir != 'LEFT ':
        dir = 'RIGHT'

    if dir == 'UP':
        snake_head[1] -= 10
    if dir == 'DOWN':
        snake_head[1] += 10
    if dir == 'LEFT':
        snake_head[0] -= 10
    if dir == 'RIGHT':
        snake_head[0] += 10

    snake_body.insert(0, list(snake_head))
    if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
        score+=10
        food = False
    else:
        snake_body.pop()

    if not food:
        food_pos =  [random.randrange(1,(600//10))*10, random.randrange(1,(500//10))*10]

    food = True
    screen.fill('black')

    for pos in snake_body:
        pygame.draw.rect(screen, 'green', (pos[0], pos[1], 10, 10))
    pygame.draw.circle(screen, 'dark red', (food_pos[0], food_pos[1]), 5)

    if snake_head[0] < 0 or snake_head[0] > 600-10:
        game_over()
    if snake_head[1] < 0 or snake_head[1] > 500-10:
        game_over()
    for block in snake_body[1:]:
        if snake_head[0] == block[0] and snake_head[1] == block[1]:
            game_over()
    
    show_score()

    pygame.display.update()
    clock.tick(snake_speed)