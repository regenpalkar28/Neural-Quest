import pygame
import noise
import random

from camera_movement import move_player_camera
from settings import TRANSITION_MODE
from region_movement import move_player_region

WIDTH, HEIGHT = 1000,1000
TILE_SIZE = 10
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

viewport_Width=WIDTH
viewport_height=HEIGHT
current_region=(0,0)
region_width=COLS
region_height= ROWS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural World Generation")
clock = pygame.time.Clock()
TREE_SIZE=16

tree_img=pygame.image.load("mtree.png").convert_alpha()
tree_width=TILE_SIZE*4
tree_height=TILE_SIZE*8

tree_img=pygame.transform.scale(tree_img,(tree_width, tree_height))

TILE_COLORS = {
   
    0:(0, 0, 139), # deepocean
    1:(2,3,145),     #ocean
    2:(0,155,255),   #shallow water
    3:(237,201,175), #beach
    4:(50,205,50), #grassland
    5:(34,139,34), #forest
    6:(139,137,137), #mountain
    7:(220,220,220)



}
def draw_player(player,camera):
    screen_x=player["x"]*TILE_SIZE-camera["x"]
    screen_y=player["y"]*TILE_SIZE-camera["y"]    

    rect=pygame.Rect(screen_x,screen_y, TILE_SIZE*4, TILE_SIZE*4)
    pygame.draw.rect(screen,(255,0,0),rect)

def generate_world(seed):
    world = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    scale = 100

    for y in range(ROWS):
        for x in range(COLS):
            n = noise.pnoise2((x+seed)/scale, (y+seed)/scale, octaves=4,
                              persistence=0.5,
                              lacunarity=2.0)
            
            
            n = (n + 1) / 2.0 
            if n < 0.2:
                tile = 0  # deepocean
            elif n<0.3:
                tile=1  #ocean  
            elif n < 0.4:
                tile = 2  # shallow water
            elif n < 0.45:
                tile = 3      #beach
            elif n<0.60:
                tile=4  #grassland
            elif n<0.70:
                tile=5 #forest
            elif n<0.85:
                tile=6      # mountain   
            else:
                tile = 7  # mountain
            world[y][x] = tile
    return world

def  place_trees(world,seed):
    random.seed(seed)
    trees=set()
    scale=70
    min_distance=20

    for y in range(ROWS):
        for x in range(COLS):
            if world[y][x]==4:
                tree_noise=noise.pnoise2((x+seed*2)/scale,
                                         (y+seed*2)/scale )
                tree_noise=(tree_noise+1)/2.0

                if tree_noise>0.30:
                    too_close=False
                    for(tx,ty) in trees:
                        if abs(x-tx)<=min_distance  and abs(y-ty)<=min_distance:
                            too_close=True
                            break
                                
                    if not too_close:
                        trees.add((x,y))
    return trees 
    

def draw_world(world,camera):
    for y in range(ROWS):
        for x in range(COLS):
            tile = world[y][x]
            color = TILE_COLORS[tile]
            rect = pygame.Rect(x*TILE_SIZE-camera["x"],
                                y*TILE_SIZE-camera["y"],
                                  TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_trees(trees,camera):
    for(x,y) in trees:
        screen.blit(tree_img, (x*TILE_SIZE-camera["x"],
                                y*TILE_SIZE-camera["y"]-(tree_img.get_height()-TILE_SIZE)))   

def load_region(region):
    rx,ry=region

    region_seed= seed+rx*1000+ry*1000
    new_world=generate_world(region_seed)
    new_trees=place_trees(new_world, region_seed)
    return new_world,new_trees

def handle_input():
    keys=pygame.key.get_pressed()
    dx,dy=0,0
    if keys[pygame.K_LEFT]: dx=-1
    if keys[pygame.K_RIGHT]: dx=1
    if keys[pygame.K_UP]: dy=-1
    if keys[pygame.K_DOWN]: dy=1
    return dx,dy


def main():
    global seed
    global current_region
    running = True
    seed = random.randint(0, 10000)
    world = generate_world(seed)
    trees=place_trees(world,seed)

    player={"x":COLS//2, "y":ROWS//2}
    camera={"x":player["x"]*TILE_SIZE-viewport_Width//2, 
            "y":player["y"]*TILE_SIZE-viewport_height//2}

    while running:
        screen.fill((0, 0, 0))
        draw_world(world,camera)
        draw_trees(trees,camera)
        draw_player(player,camera)

        dx,dy=handle_input()
        move_player_camera(player,camera,dx,dy, viewport_Width, viewport_height,margin=5,world=world,trees=trees,tile_size= TILE_SIZE)
        current_region , new_world, new_trees=move_player_region(player,dx,dy,current_region,region_width, region_height,load_region)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                seed = random.randint(0, 10000)
                world = generate_world(seed)
                trees=place_trees(world,seed)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()