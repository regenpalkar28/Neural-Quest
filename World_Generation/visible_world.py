import math 
import random
import pygame 
from sys import exit
import numpy as np

master_height, master_width = 12000, 12000

window_size = 600
screen_height, screen_width = window_size, window_size
minimap_size = window_size*0.3
bigpixel_size = 60  # Each "terrain pixel" is 120x120 screen pixels
grid_size = 50   # Perlin noise grid size

# Calculate how many big pixels we have
bigpixel_height = master_height // bigpixel_size  # 100 bigpixels
bigpixel_width = master_width // bigpixel_size    # 100 bigpixels

visible_bp_x = int(screen_width*2  // bigpixel_size)   # number of bigpixels that fit horizontally
visible_bp_y = int(screen_height*2 // bigpixel_size)  # number of bigpixels that fit vertically

max_window_x = bigpixel_width - visible_bp_x    # so that window does not go out of bounds
max_window_y = bigpixel_height - visible_bp_y   

min_noise = float('inf')
max_noise = float('-inf')
noise_map = np.zeros((bigpixel_height, bigpixel_width), dtype=float)
world_map = np.zeros((bigpixel_height, bigpixel_width), dtype=np.uint8)  

gradient_grid = {}

def gradient(x):
    """ Generates a gradient vector """
    return math.cos(x), math.sin(x)
def lerp(a,b,x):
    """ Linear Interpolation. """
    return a + x*(b-a)
def fade(t):
    """ Smoothstep Interpolation. """
    return  t * t * t * (t * (t * 6 - 15) + 10)

for gx in range(bigpixel_width + 1):
    for gy in range(bigpixel_height + 1):
        gradient_grid[(gx, gy)] = gradient(random.random()* 2*math.pi)

def perlin(bpx, bpy, grid_size):
    """ This function will generate perlin noise values for bigpixel x, and bigpixel y"""
    x0, y0 = int(bpx//grid_size), int(bpy//grid_size)
    x1, y1 = x0 +1, y0+1

    dx, dy = bpx/grid_size - x0, bpy/grid_size - y0

    grad00 = gradient_grid[(x0, y0)]
    grad10 = gradient_grid[(x1, y0)]
    grad01 = gradient_grid[(x0, y1)]
    grad11 = gradient_grid[(x1, y1)]

    dot00 = grad00[0] * dx + grad00[1] * dy
    dot10 = grad10[0] * (dx - 1) + grad10[1] * dy
    dot01 = grad01[0] * dx + grad01[1] * (dy - 1)
    dot11 = grad11[0] * (dx - 1) + grad11[1] * (dy - 1)
    
    u, v = fade(dx), fade(dy)
    return lerp(lerp(dot00, dot10, u) , lerp(dot01, dot11, u), v)

def octave_perlin(x, y, octaves=4, persistence=0.5):
    total = 0
    frequency = 1
    amplitude = 1
    max_value = 0
    for _ in range(octaves):
        total += perlin(x * frequency, y * frequency, grid_size) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= 2
    return total / max_value

for bpy in range(bigpixel_height):
  for bpx in range(bigpixel_width):
      scale = 3
      noise_value = perlin(bpx*scale, bpy*scale, grid_size)
      noise_map[bpy][bpx] = noise_value
      min_noise = min(min_noise, noise_value)
      max_noise = max(max_noise, noise_value)

cx, cy = bigpixel_width/2, bigpixel_height/2
image = np.zeros((master_height, master_width, 3), dtype=np.uint8)

def terrain_type(bpx,bpy):
    """ 
    This determines the terrain type based on the noise layers
    """
    normalized_noise = (noise_map[bpy][bpx] - min_noise) / (max_noise - min_noise)
    dx = (bpx - cx) / cx
    dy = (bpy - cy) / cy

    distance = math.sqrt(dx*dx + dy*dy)
    falloff = max(0, 1 - distance)
    val = normalized_noise * falloff

    if val < 0.05:
        terrain = "OCEAN"
    elif val < 0.07:
        terrain = "SHALLOW"
    elif val < 0.1:
        terrain = "SAND"
    elif val < 0.45:
        terrain = "PLAINS"
    elif val < 0.65:
        terrain = "HIGHLAND_PLAINS"
    elif val < 0.7:
        terrain = "MOUNTAIN"
    else:
        terrain = "MOUNTAIN_PEAK"
    return terrain

def generate_world_map(bp_width, bp_height):
    """ Generates the 2D map with the help of terrain_type()"""
    terrain_ids = {
        "OCEAN": 0,
        "SHALLOW": 1,
        "PLAINS": 2,
        "HIGHLAND_PLAINS": 3,
        "MOUNTAIN": 4,
        "MOUNTAIN_PEAK": 5,
        "SAND" : 6
    }

    for y in range(bp_height):
        for x in range(bp_width):
            terrain = terrain_type(x,y)
            world_map[y,x] = terrain_ids[terrain]
    return world_map

TERRAIN_COLORS = {
    5 :(184, 216, 230),       # MOUNTAIN PEAK, Light Grey
    4: (75, 94, 87),          # MOUNTAIN, Dark Grey
    2: (139, 222, 44),        # PLAINS, Green
    3: (91, 130, 47),         # HIGHLAND_PLAINS, Greyish-Green
    1: (74, 122, 199),        # SHALLOW, Blue
    0: (40, 69, 115),          # OCEAN, Dark blue
    6: (199, 182, 135)        # SAND, Ochre 
}

def minimap(world_map):
    raw_surface = pygame.Surface((bigpixel_width, bigpixel_height))
    px_array = pygame.PixelArray(raw_surface)
    for y in range(bigpixel_height):
        for x in range(bigpixel_width):
            terrain_id = world_map[y, x]
            color = TERRAIN_COLORS[terrain_id]
            
            px_array[x, y] = raw_surface.map_rgb(color)
    del px_array
    return pygame.transform.scale(raw_surface, (minimap_size, minimap_size))


def viewport(minimap_surface, window_x, window_y, color=(255,0,0), thickness=2):
    minimap_tile_x = minimap_size / bigpixel_width
    minimap_tile_y = minimap_size / bigpixel_height

    rect_x = window_x * minimap_tile_x
    rect_y = window_y * minimap_tile_y
    rect_w = visible_bp_x * minimap_tile_x
    rect_h = visible_bp_y * minimap_tile_y
    pygame.draw.rect(minimap_surface, color, pygame.Rect(rect_x, rect_y, rect_w, rect_h), thickness)

def display_world(surface, world_map, top_left=(0,0)):
    bpx_offset, bpy_offset = top_left
    
    global visible_bp_x, visible_bp_y
    visible_bp_x = screen_width // bigpixel_size
    visible_bp_y = screen_height // bigpixel_size

    for y in range(visible_bp_y):
        world_y = bpy_offset + y
        for x in range(visible_bp_x):
            world_x = bpx_offset + x
            terrain = world_map[world_y, world_x]
            color = TERRAIN_COLORS[terrain]
            rect = pygame.Rect(
                x * bigpixel_size,
                y * bigpixel_size,
                bigpixel_size,
                bigpixel_size
            )
            pygame.draw.rect(surface, color, rect)
print("Generating World")
world_map = generate_world_map(bigpixel_width, bigpixel_height)
print("World Generated..")
minimap_surface_OG = minimap(world_map)

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('World Generation')
clock = pygame.time.Clock()

window_x, window_y=0,0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                window_x = max(window_x-visible_bp_x, 0)
            elif event.key == pygame.K_RIGHT:
                window_x = min(window_x + visible_bp_x, max_window_x)
            elif event.key == pygame.K_UP:
                window_y = max(window_y-visible_bp_y, 0)
            elif event.key == pygame.K_DOWN:
                window_y = min(window_y+visible_bp_y, max_window_y)

    minimap_surface = minimap_surface_OG.copy()

    viewport(minimap_surface, window_x, window_y) 
    screen.blit(minimap_surface, (screen_width - minimap_size - 10, 10))
    screen.fill((0,0,0))
    display_world(screen, world_map, top_left=(window_x,window_y))

    screen.blit(minimap_surface, (screen_width - minimap_size - 10, 10))
    border_color = (255, 255, 255)  # White border
    border_width = 2                # Thickness in pixels
    pygame.draw.rect(
        screen,
        border_color,
        pygame.Rect(
            screen_width - minimap_size - 10,  # x-position
            10,                                 # y-position
            minimap_size,                       # width
            minimap_size                        # height
        ),
        border_width
    )
    
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)


