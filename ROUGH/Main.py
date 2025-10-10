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

print("Generating World..")
subprocess.run([venv_python, 'world_generator.py'], check=True)
print("World Generated")

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

text_panel_width = 400

world_map_npy_path = os.path.join(os.getcwd(), 'world_map.npy')
world_map_tid_npy = np.load(world_map_npy_path)

world_map_colored_path = os.path.join(os.getcwd(), 'world_map_colored.npy')
world_map_colored = np.load(world_map_colored_path)

world_map = Image.fromarray(world_map_colored)

pygame.init()
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

        self.speed = 2
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
        self.id = id
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
        self.waiting_message = "I can't talk to you yet."
        self.activenpc = None

        self.dialogue_active = False
        self.dialogue_text = ""
        self.ok_button_rect = pygame.Rect(220, 440, 80, 30)

        self.npc_states = {
            f"NPC_{i}": {
                "dialogue": None,          # what the NPC says (left-side box)
                "mission_text": None,      # story/narration (right panel)
                "is_generating": False,    # if LLM generation is ongoing
                "is_ready": False,          # if this NPC’s dialogue/story is generated
                "has_been_triggered": False
            }
            for i in range(1, char_num + 1)
        }
        
    def check_trigger(self, protagonist):
        if self.current_idx >= len(self.npc_sequence):
            return

        current_npc = self.npc_sequence[self.current_idx]
        next_npc = (
            self.npc_sequence[self.current_idx + 1] 
            if self.current_idx + 1 < len(self.npc_sequence) 
            else None
        )
        current_state = self.npc_states[f"NPC_{current_npc.id}"]

        #Prot meets current NPC
        if protagonist.rect.colliderect(current_npc.rect):
            if not current_state.get("has_been_triggered", False) and not current_state.get("is_generating", False):
                self.activenpc = current_npc
                current_state["is_generating"] = True

                self.dialogue_text = f"{current_npc.name}: Generating response..."
                self.dialogue_active = True

                # Call LLM to generate dialogue & story
                self.generate_npc_mission(current_npc, next_npc)

                # After generation
                current_state["has_been_triggered"] = True
                current_state["is_generating"] = False
                self.dialogue_text = current_state.get("dialogue", "")
                self.current_idx += 1
        #Prot meets wrong NPC
        elif not current_state.get("is_generating", False) and not self.dialogue_active:
            near_other = False
            for npc in self.npc_sequence:
                if npc != current_npc and protagonist.rect.colliderect(npc.rect):
                    npc_state = self.npc_states[f"NPC_{npc.id}"]
                    if not npc_state.get("waiting_shown", False):
                        self.dialogue_active = True
                        self.dialogue_text = f"{npc.name}: {self.waiting_message}"
                        npc_state["waiting_shown"] = True
                    near_other = True
                    break

            if not near_other:
                self.current_story = ""
                self.activenpc = None

    # resetting waiting_shown for NPCs not near protagonist 
        for npc in self.npc_sequence:
            if not protagonist.rect.colliderect(npc.rect):
                npc_state = self.npc_states[f"NPC_{npc.id}"]
                npc_state["waiting_shown"] = False

    def generate_npc_mission(self, npc, npc_next):
        with open(self.storyfile, "r", encoding='utf-8') as f:
            story = f.read()
        prot_name = self.protagonist_info["name"]
        prot_role = self.protagonist_info["role"]
        npc_state = self.npc_states[f"NPC_{npc.id}"]
        npc_state["is_generating"] = True

        prompt = f"""
        "{story}"

        Continue the fantasy kingdom story. Remember that this encounter takes place on an island. 

        The protagonist, {prot_name}, a {prot_role} meets {npc.name}, a {npc.appearance['age']}-year old {npc.appearance['gender']}, who {npc.role}.
        Describe this encounter in 30-50 words, keeping the story continuous.

        Return EXACTLY TWO separate sections, with no extra text:
        The two sections must start with 1. DIALOGUE: <text> and 2. STORY: <text>
        1. DIALOGUE (first person, what {npc.name} actually says to the {prot_name}):
        - Use 1-3 short, clear sentences.
        - Do NOT add any narrative, descriptions, or actions—only the words spoken.
        - Include instructions to the protagonist (e.g., where to go next) here.

        2. STORY (third person, for telling an outside viewer what happened):
        - Summarize the encounter in 3-5 sentences.
        - Use continuous narrative.
        - Include the NPC's actions, appearance, and any relevant guidance.
        - Do NOT include direct speech here.

        """
        if npc_next:
            prompt += f"""
            At the end, the protagonist should be told to meet {npc_next.name}, a {npc_next.role}.
            Add this in the DIALOGUE part."""

        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-120b:cerebras",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_op = response.choices[0].message.content

        npc_state["is_generating"] = False
        # parsing raw output
        dialogue_text = ""
        story_text = ""

        dialogue_start = raw_op.index("1. DIALOGUE")
        story_start = raw_op.index("2. STORY")

        dialogue_text = raw_op[dialogue_start + len("1. DIALOGUE"):story_start].strip()
        story_text = raw_op[story_start + len("2. STORY"):].strip(" :\n")

        npc_state["mission_text"] = story_text
        npc_state["dialogue"] = dialogue_text
        npc_state["is_ready"] = True
        self.dialogue_text = dialogue_text
        self.current_story = story_text

        with open(self.storyfile, "a", encoding="utf-8") as f:
            f.write("\n" + story_text)

def text_render(surface, text, x, y, width, font, color=(255, 255, 255)):
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test = (current_line + word + " ").strip()
        if font.size(test)[0] < width:
            current_line = test + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
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

# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if storyline_instance.dialogue_active and storyline_instance.ok_button_rect.collidepoint(event.pos):
                storyline_instance.dialogue_active = False
                storyline_instance.dialogue_text = ""

    keys = pygame.key.get_pressed()
    if not storyline_instance.dialogue_active:
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
    if storyline_instance.current_idx < len(storyline_instance.npc_sequence):
        next_npc = storyline_instance.npc_sequence[storyline_instance.current_idx]
        next_x = next_npc.rect.x * minimap_size / master_dim
        next_y = next_npc.rect.y * minimap_size / master_dim
        pygame.draw.circle(minimap_copy, (235, 235, 52), (int(next_x), int(next_y)), 5)
    screen.blit(minimap_copy, (win_size - minimap_size - 10, 10))
    
    storyline_instance.check_trigger(Prot1)
    # text 
    pygame.draw.rect(screen, (20, 20, 20), (win_size, 0, text_panel_width, win_size))  
    pygame.draw.rect(screen, (100, 100, 100), (win_size, 0, text_panel_width, win_size), 2)
    text_font = pygame.font.SysFont("constantia", 16)
    text_render(screen, storyline_instance.current_story, win_size + 10, 10, text_panel_width - 20, text_font)

    if storyline_instance.activenpc:
        npc_id = storyline_instance.activenpc.id
        npc_state = storyline_instance.npc_states[f"NPC_{npc_id}"]
        if npc_state["is_generating"]:
            generating_text = text_font.render("Generating response...", True, (255, 0, 0))
            screen.blit(generating_text, (win_size + 10, 10))
    if storyline_instance.dialogue_active:
        dialogue_rect = pygame.Rect(50, 350, 350, 120)  
        pygame.draw.rect(screen, (30, 30, 30), dialogue_rect)
        storyline_instance.ok_button_rect.topleft = (dialogue_rect.right - 90, dialogue_rect.bottom - 35)
        pygame.draw.rect(screen, (100, 200, 100), storyline_instance.ok_button_rect) 

        text_render(screen, storyline_instance.dialogue_text, dialogue_rect.x + 10, dialogue_rect.y + 10,
                    dialogue_rect.width - 20, text_font)

        # Draw OK text
        ok_text = text_font.render("OK", True, (0, 0, 0))
        screen.blit(ok_text, (storyline_instance.ok_button_rect.x + 30, storyline_instance.ok_button_rect.y + 10))
    pygame.display.flip()