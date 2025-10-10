import math 
import random
import numpy as np
import os
from PIL import Image

master_dim = 12000
win_size = 600

minimap_size = win_size*0.3     
bp_size = 60  
noise_grid_size = 90  # Perlin noise grid size


bp_num = master_dim // bp_size  # 200 bigpixels
 
min_noise = float('inf')
max_noise = float('-inf')
noise_map = np.zeros((bp_num, bp_num), dtype=float)
world_map = np.zeros((bp_num, bp_num), dtype=np.uint8)  

gradient_grid = {}

def gradient(x):
    """ Generates a gradient vector """
    return math.cos(x), math.sin(x)
def lerp(a,b,x):
    """ Linear Interpolation. """
    return a + x*(b-a)
def fade(t):
    """ Smoothstep Interpolation. """
    return  (6*(t**2) - 15*t + 10)*(t**3)

for gx in range(bp_num + 1):
    for gy in range(bp_num + 1):
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

def octave_perlin(x, y, octaves=5, persistence=0.5):
    total = 0
    frequency = 1
    amplitude = 1
    max_value = 0
    for _ in range(octaves):
        total += perlin(x * frequency, y * frequency, noise_grid_size) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= 2
    return total / max_value

for bpy in range(bp_num):
  for bpx in range(bp_num):
      scale = 3
      noise_value = octave_perlin(bpx*scale, bpy*scale)
      noise_map[bpy][bpx] = noise_value
      min_noise = min(min_noise, noise_value)
      max_noise = max(max_noise, noise_value)

cx, cy = bp_num/2, bp_num/2

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
    elif val < 0.56:
        terrain = "HIGHLAND_PLAINS"
    elif val < 0.67:
        terrain = "MOUNTAIN"
    else:
        terrain = "MOUNTAIN_PEAK"
    return terrain

def generate_world_map():
    """ Generates the 2D map with the help of terrain_type()"""
    terrain_ids = {
        "OCEAN": 0,
        "SHALLOW": 1,
        "SAND":2,
        "PLAINS": 3,
        "HIGHLAND_PLAINS":4,
        "MOUNTAIN":5,
        "MOUNTAIN_PEAK":6
        }

    for y in range(bp_num):
        for x in range(bp_num):
            terrain = terrain_type(x,y)
            world_map[y,x] = terrain_ids[terrain]
    return world_map

world_map = generate_world_map()
upscaled_map = np.repeat(np.repeat(world_map, bp_size, axis=0), bp_size, axis=1)

print(f"saving world map to: {os.path.join(os.getcwd(), 'world_map.npy')}")
np.save('world_map.npy', upscaled_map)

TERRAIN_COLORS = np.array([
    [27, 65, 125],       # OCEAN
    [43, 95, 179],       # SHALLOW
    [168, 163, 138],     # SAND
    [137, 173, 101],     # PLAINS
    [123, 140, 107],     # HIGHLAND_PLAINS
    [77, 82, 72],        # MOUNTAIN
    [201, 204, 198]      # MOUNTAIN_PEAK
    ], dtype=np.uint8)

tiles_folder = os.path.join(os.getcwd(), 'MAPTILES')
TERRAIN_IMG = {
    0: os.path.join(tiles_folder, 'OCEAN.png'),
    1: os.path.join(tiles_folder, 'SHALLOW.png'),
    2: os.path.join(tiles_folder, 'SAND.png'),
    3: os.path.join(tiles_folder, 'PLAINS.png'),
    4: os.path.join(tiles_folder, 'HIGHLAND_PLAINS.png'),
    5: os.path.join(tiles_folder, 'MOUNTAIN.png'),
    6: os.path.join(tiles_folder, 'MOUNTAIN_PEAK.png')
    }    

world_image = TERRAIN_COLORS[upscaled_map]
np.save('world_map_colored.npy', world_image)

world_img_file = Image.fromarray(world_image)
world_img_file.save("world_map.png")

master_image = Image.new("RGB", (master_dim, master_dim))

loaded_tiles = {}

for terrain_id, file_path in TERRAIN_IMG.items():
    loaded_tiles[terrain_id] = Image.open(file_path).convert("RGB")

for y in range(bp_num):
    for x in range(bp_num):
        terrain_id = world_map[y,x]

        tile_image = loaded_tiles.get(terrain_id)
        paste_x = x*bp_size
        paste_y = y*bp_size

        master_image.paste(tile_image, (paste_x, paste_y))

master_image.save("world_map_tiled.png")
