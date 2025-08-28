import pygame
pygame.init()

turn = 'X'
winner = None
draw = None

board = [[None]*3, [None]*3, [None]*3]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400,400))

ximg = pygame.image.load(r'Pygame Tutorial\Images\X.png')
oimg = pygame.image.load(r'Pygame Tutorial\Images\O.png')

ximg = pygame.transform.scale(ximg, (80,80))
oimg = pygame.transform.scale(oimg, (80,80))

def draw_grid():
    screen.fill((255,255,255))

    pygame.draw.line(screen, (0,0,0), (400/3, 0), (400/3, 400), 6) #first vertical
    pygame.draw.line(screen, (0,0,0), (800/3, 0), (800/3, 400), 6) #second vertical

    pygame.draw.line(screen, (0,0,0), (0, 400/3), (400, 400/3), 6) #first horizontal
    pygame.draw.line(screen, (0,0,0), (0, 800/3), (400, 800/3), 6) #second horizontal

def result():
    global draw, winner
    if winner:
        message=winner+" won!"
    if draw:
        message="Game draw!"
    
    font = pygame.font.SysFont('Georgia', 70)
    text = font.render(message, 1, (24,185,35))
    screen.fill((0,0,0), (0,400,500,100))
    text_rect = text.get_rect(center=(200,200))
    screen.blit(text, text_rect)
    pygame.display.update()

def wincases():
    global board, winner, draw
    for row in range(0,3): #checking all rows
        if ((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] != None)):
            winner = board[row][0]
            pygame.draw.line(screen, (250,0,0), (0,(row+1)*400/3 - 400/6), (400, (row+1)*400/3 -400/6),4)
            result()
            break

    for col in range(0,3): # checking all cols
        if ((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] != None)):
            winner = board[0][col]
            pygame.draw.line(screen, (250,0,0), ((col+1)*400/3 - 400/6, 0), ((row+1)*400/3 -400/6,400), 4)
            result()
            break 
    
    #checking diag 1
    if (board[0][0] == board[1][1] == board[2][2] ) and board[0][0]!= None:
        winner = board[0][0]
        pygame.draw.line(screen, (250,70,70), (50,50), (350,350), 4)
        result()
    #checking diag2    
    if (board[0][2] == board[1][1] == board[2][0] ) and board[0][2]!= None:
        winner = board[0][2]
        pygame.draw.line(screen, (250,70,70), (350,50), (50,350), 4)
        result()
    if(all([all(row) for row in board]) and winner==None):
        draw = True
        result()


def getimg(row,col):
    global board, turn

    if row==1:
        pos_y = 30
    if row ==2:
        pos_y = 30 + 400/3
    if row ==3:
        pos_y = 30 + 800/3
    if col ==1:
        pos_x = 30
    if col ==2:
        pos_x = 30 + 400/3
    if col ==3:
        pos_x = 30 + 800/3

    board[row-1][col-1 ] = turn

    if turn == 'X':
        screen.blit(ximg, (pos_x, pos_y))
        turn = 'O'
    else:
        screen.blit(oimg, (pos_x, pos_y))
        turn = 'X'
    pygame.display.update()

def input_to_block():
    x,y = pygame.mouse.get_pos()

    if(x<400/3):
        col=1
    elif(x<800/3):
        col=2
    elif(x<400):
        col=3
    else:
        col = None

    if(y<400/3):
        row=1
    elif(y<800/3):
        row=2
    elif(y<400):
        row=3
    else:
        row = None

    if(row and col and board[row-1][col-1] is None):
        global turn
        getimg(row,col)
        wincases()
    
draw_grid()

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            exit()
        elif events.type == pygame.MOUSEBUTTONDOWN:
            input_to_block()
    
    pygame.display.update()
    clock.tick(30)