import subprocess
import numpy as np
from PIL import Image
import pygame
import os

pygame.init()
pygame.display.init()

WORLD_GENERATOR = 'world_generator.py'

print("Generating World...")
subprocess.run(['python', WORLD_GENERATOR], check=True)
world_file_path = 'world_map.npy'

world_map = np.load(world_file_path)

master_dim = 12000
win_size = 600
minimap_size = 0.3*win_size  # 180
bp_size = 60
bp_num = master_dim // bp_size      # 200 bps in total
visible_bp = win_size*2  // bp_size  # 20 bp's == 1200 pixels

screen = pygame.display.set_mode((win_size, win_size), pygame.RESIZABLE)
pygame.display.set_caption("Spawning Characters")
TERRAIN_COLORS = np.array([
    [27, 65, 125],       # OCEAN
    [43, 95, 179],       # SHALLOW
    [168, 163, 138],     # SAND
    [137, 173, 101],     # PLAINS
    [123, 140, 107],     # HIGHLAND_PLAINS
    [77, 82, 72],        # MOUNTAIN
    [201, 204, 198]      # MOUNTAIN_PEAK
    ], dtype=np.uint8)

world_image = TERRAIN_COLORS[world_map]
world_img_file = Image.fromarray(world_image, "RGB")
world_img_file.save("world_map.png")

world_surface = pygame.Surface((bp_num, bp_num))
world_surface = pygame.surfarray.make_surface(world_image.transpose(1,0,2))
world_surface = pygame.transform.scale(world_surface, (master_dim, master_dim))

class Camera:
    def __init__(self,width, height):
        self.rect = pygame.Rect(0,0,width,height)
    def apply(self, Prot):
        return Prot.rect.move(-self.rect.topleft[0], -self.rect.topleft[1])
    def update(self, target):
        x = target.rect.centerx - win_size//2
        y = target.rect.centery - win_size//2
        x = max(0, min(x, master_dim - win_size))
        y = max(0, min(y, master_dim - win_size))
        self.rect.topleft = (x, y)

camera = Camera(master_dim, master_dim)

protagonist_png = os.path.join(os.getcwd(), 'Images', 'knight.png')

def spawn_location(world_map):
    y , x = np.where(world_map == 3)
    idx = np.random.randint(0, len(x))
    return x[idx]*bp_size, y[idx]*bp_size

def can_move(x,y):
    if world_map[y,x]==0 or world_map[y,x]==1 or world_map[y,x]==6:
        return False
    else:
        return True

def draw_viewport(minimap, camera):
    scale = minimap_size / master_dim
    rect = pygame.Rect(
        camera.rect.x * scale,
        camera.rect.y * scale,
        win_size * scale,
        win_size * scale
    )
    pygame.draw.rect(minimap, (255,0,0), rect, 2)

class Protagonist:
    def __init__(self, x,y):
        self.width = int(win_size*0.1)
        self.height = int(win_size*0.1)
        self.size = (self.width, self.height)

        self.front = pygame.image.load(protagonist_png).convert_alpha() # for transparent png's
        self.front = pygame.transform.scale(self.front, self.size)
        self.right = pygame.transform.flip(self.front, True, False)

        self.image = self.front  # current orientation
        self.rect = self.image.get_rect(topleft = (x,y))

        self.speed = 1
        self.facing = "left"
    
    def move(self, dx=0, dy=0):
        bp_x = (self.rect.x + dx)//bp_size
        bp_y = (self.rect.y + dy)//bp_size 

        if can_move(bp_x, bp_y):

            self.rect.x += dx
            self.rect.y += dy

            # flip image based on direction
            if dx > 0:
                self.image = self.right
                self.direction = "right"
            elif dx < 0:
                self.image = self.front
                self.direction = "left/front"
        
    def draw(self, surface, camera):
        surface.blit(self.image, (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y))

spawn_x, spawn_y = spawn_location(world_map)
Prot1 = Protagonist(spawn_x, spawn_y)

minimap_surface = pygame.image.load("world_map.png").convert()
minimap_surface = pygame.transform.scale(minimap_surface, (minimap_size, minimap_size))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Prot1.image = Prot1.front
        Prot1.facing = "left"
        Prot1.move(-Prot1.speed,0)
    elif keys[pygame.K_d]:
        Prot1.image = Prot1.right
        Prot1.facing = "right"
        Prot1.move(Prot1.speed,0)
    elif keys[pygame.K_w]:
        Prot1.image = Prot1.front if Prot1.facing == "left" else Prot1.right 
        Prot1.move(0,-Prot1.speed)
    elif keys[pygame.K_s]:
        Prot1.image = Prot1.front if Prot1.facing == "left" else Prot1.right
        Prot1.move(0, Prot1.speed)

    camera.update(Prot1)
    screen.fill((0,0,0))

    source_visible_rect = pygame.Rect(
    camera.rect.x,
    camera.rect.y,
    win_size,
    win_size
    )

    # scaling this to the window size
    visible_surface = world_surface.subsurface(source_visible_rect)

    screen.blit(visible_surface, (0,0))
    Prot1.draw(screen, camera)

    minimap_copy = minimap_surface.copy()
    draw_viewport(minimap_copy, camera)
    screen.blit(minimap_copy, (win_size - minimap_size - 10, 10))
    
    pygame.display.flip()


