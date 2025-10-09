import os
import sys
import subprocess
import pygame
import numpy as np
from PIL import Image
import json
from dotenv import load_dotenv
from openai import OpenAI
from huggingface_hub import login

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
login(hf_token)

venv_python = os.path.join(sys.prefix, 'Scripts', 'python.exe')

# print("Generating World..")
# subprocess.run([venv_python, 'world_generator.py'], check=True)
# print("World Generated")

# print("\nTaking User Input for Protagonist..")
# subprocess.run([venv_python, 'Protagonist_User_Input.py'], check=True)

# print("\nCleaning and completing Information..")
# subprocess.run([venv_python, 'Prot_Info_Complete.py'], check=True)

# print("\nGenerating Sprite for Protagonist...")
# subprocess.run([venv_python, 'Protagonist_SpritePixelLab.py'], check=True)
# # uncomment the above to demonstrate a fresh image generation.

# print("\n Removing Background Color..")
# subprocess.run([venv_python, 'Prot_BG_remove.py'], check=True)

# # generating initial storyline 
# subprocess.run([venv_python, 'InitialStoryline.py'], check=True)

# # generating character data
# subprocess.run([venv_python, 'NPC_info.py'], check=True)
# print("Generated character data")

# # generating character sprites
# subprocess.run([venv_python, 'NPCSprites.py'], check=True)
# print("Generated character Images")
# # keep the above uncommented to demonstrate a fresh image generation

# subprocess.run([venv_python, 'NPC_BG_remove.py'], check=True)

master_dim = 12000
win_size = 600
bp_size = 60
minimap_size = win_size*0.3

text_panel_width = 200

world_map_npy_path = os.path.join(os.getcwd(), 'world_map.npy')
world_map_tid_npy = np.load(world_map_npy_path)

world_map_colored_path = os.path.join(os.getcwd(), 'world_map_colored.npy')
world_map_colored = np.load(world_map_colored_path)

world_map = Image.fromarray(world_map_colored)

pygame.display.init()
screen = pygame.display.set_mode((win_size+text_panel_width, win_size), pygame.RESIZABLE)

world_surface = pygame.Surface((master_dim, master_dim))
world_surface = pygame.surfarray.make_surface(world_map_colored.transpose(1,0,2))

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

protagonist_png = os.path.join(os.getcwd(), 'Characters', 'protagonist.png')

def spawn_location(world_map_npy):
    y , x = np.where(world_map_npy == 3)
    idx = np.random.randint(0, len(x))
    return x[idx], y[idx]

def can_move(x,y):
    
    terrain_id = world_map_tid_npy[y, x]

    if terrain_id in [0,1,6]:
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

with open("Characters/protagonist_info.json", "r", encoding="utf-8") as f:
    protagonist_info = json.load(f)

class Protagonist:
    def __init__(self, x,y, info):
        self.width = int(win_size*0.2)
        self.height = int(win_size*0.2)
        self.size = (self.width, self.height)

        self.left = pygame.image.load(protagonist_png).convert_alpha() # for transparent png's
        self.left = pygame.transform.scale(self.left, self.size)
        self.right = pygame.transform.flip(self.left, True, False)

        self.image = self.left  # current orientation
        self.rect = self.image.get_rect(topleft = (x,y))

        self.speed = 1
        self.facing = "left"
    
        self.info = info
    def move(self, dx=0, dy=0):

        if can_move(self.rect.x + self.width//2 + dx, self.rect.y + self.height + dy):

            self.rect.x += dx
            self.rect.y += dy

            # flip image based on direction
            if dx > 0:
                self.image = self.right
                self.direction = "right"
            elif dx < 0:
                self.image = self.left
                self.direction = "left"
        
    def draw(self, surface, camera):
        surface.blit(self.image, (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y))
               
NPC_IMG = []
char_num = 5
for i in range(char_num):
    NPC_IMG.append(os.path.join(os.getcwd(), 'Characters', f'NPC_{i+1}.png'))

class NPC:
    def __init__(self, x,y, id, npc_data):
        self.width = int(win_size*0.25)
        self.height = int(win_size*0.25)
        self.size = (self.width, self.height)

        self.img = pygame.image.load(NPC_IMG[id-1]).convert_alpha()
        self.rect = self.img.get_rect(topleft = (x,y))
        self.name = npc_data['name']
        self.role = npc_data['role']
        self.personality = npc_data['personality']
        self.appearance = npc_data['appearance']

    def draw(self, surface, camera):
        if self.rect.colliderect(camera.rect):
            surface.blit(self.img, (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y))
    
spawn_x, spawn_y = spawn_location(world_map_tid_npy)
Prot1 = Protagonist(spawn_x , spawn_y, protagonist_info)

NPC_Spawn = {}
npc_info_path = os.path.join(os.getcwd(), 'Characters', 'NPC.json')

with open(npc_info_path, "r", encoding='utf-8') as f:
      npc_info = json.load(f)

for i,npc_data in enumerate(npc_info):
    x, y = spawn_location(world_map_tid_npy) 
    print(f"{npc_data['name']} at ",x,y) 
    npc = NPC(x, y, i+1, npc_data)                     
    NPC_Spawn[f'NPC_{i+1}'] = npc
        

minimap_surface = pygame.image.load("world_map.png").convert()
minimap_surface = pygame.transform.scale(minimap_surface, (minimap_size, minimap_size))

class storyline:
    def __init__(self, npc_sequence, llm, protagonist_info, storyfile="story.txt"):
        self.npc_sequence = npc_sequence
        self.current_idx = 0
        self.llm = llm
        self.protagonist_info = protagonist_info
        self.storyfile = storyfile

        self.current_story = ""

    def check_trigger(self, protagonist):
        if self.current_idx >= len(self.npc_sequence):
            return
        current_npc = self.npc_sequence[self.current_idx]
        next_npc = self.npc_sequence[self.current_idx + 1] if self.current_idx + 1 < len(self.npc_sequence) else None

        if protagonist.rect.colliderect(current_npc.rect):
            print(f"Protagonist collided with {current_npc.name}")
            self.generate_npc_mission(current_npc, next_npc)
            self.current_idx += 1

            with open(self.storyfile, "r", encoding="utf-8"):
                self.current_story = f.read()

    def generate_npc_mission(self, npc, npc_next):
        with open(self.storyfile, "r", encoding='utf-8') as f:
            story = f.read()
    
        prompt = f"""
        "{story}"

        Continue the fantasy kingdom story. Remember that this encounter takes place on an island. 

        They meet {npc.name}, a {npc.appearance['age']}-year old {npc.appearance['gender']}, who {npc.role}.
        Describe this encounter in 30-50 words, keeping the story continuous.
        """
        if npc_next:
            prompt += f"\nAt the end, the protagonist should be told to meet {npc_next.name}, a {npc_next.role}."
        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-120b:cerebras",
            messages=[{"role": "user", "content": prompt}]
        )
        story_part = response.choices[0].message.content
        self.current_story = story_part

        with open(self.storyfile, "a", encoding="utf-8") as f:
           f.write("\n" + story_part)
        
def text_render(surface, text, x,y,width, font, color=(255,255,255)):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test = current_line + word
        if font.size(test)[0] < width:
            current_line = test
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * (font.get_height() + 4)))

npc_sequence = [npc for npc in NPC_Spawn.values()]
storyline_instance = storyline(
    npc_sequence=npc_sequence,
    llm = OpenAI(
    base_url="https://router.huggingface.co/v1",api_key=hf_token),
    protagonist_info=protagonist_info,
    storyfile="story.txt"
)

storyfile = "story.txt"
with open(storyfile, "r", encoding="utf-8") as f:
    story_text = f.read()


# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Prot1.image = Prot1.left
        Prot1.facing = "left"
        Prot1.move(-Prot1.speed,0)
    elif keys[pygame.K_d]:
        Prot1.image = Prot1.right
        Prot1.facing = "right"
        Prot1.move(Prot1.speed,0)
    elif keys[pygame.K_w]:
        Prot1.image = Prot1.left if Prot1.facing == "left" else Prot1.right 
        Prot1.move(0,-Prot1.speed)
    elif keys[pygame.K_s]:
        Prot1.image = Prot1.left if Prot1.facing == "left" else Prot1.right
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
    for npc in NPC_Spawn.values():
        npc.draw(screen, camera)

    minimap_copy = minimap_surface.copy()
    draw_viewport(minimap_copy, camera)
    for npc in NPC_Spawn.values():
        npc_x = npc.rect.x * minimap_size / master_dim
        npc_y = npc.rect.y * minimap_size / master_dim
        pygame.draw.circle(minimap_copy, (0, 255, 0), (int(npc_x), int(npc_y)), 3)
    screen.blit(minimap_copy, (win_size - minimap_size - 10, 10))
    
    storyline_instance.check_trigger(Prot1)
    # text 
    pygame.draw.rect(screen, (20, 20, 20), (win_size, 0, text_panel_width, win_size))  
    pygame.draw.rect(screen, (100, 100, 100), (win_size, 0, text_panel_width, win_size), 2)
    text_font = pygame.font.SysFont("constantia", 16)
    text_render(screen, storyline_instance.current_story, win_size + 10, 10, text_panel_width - 20, text_font)

    pygame.display.flip()