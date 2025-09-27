import pygame as pg
from huggingface_hub import login
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_TOKEN")
login(token)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)
pg.init()
info = pg.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)

pg.display.set_caption('NPC Interaction')
speed = int(SCREEN_WIDTH * 0.005)
x = int(SCREEN_WIDTH * 0.225)
y = int(SCREEN_HEIGHT * 0.325)  

player_size = (int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.071))
player_front = pg.image.load('Pygame Implementations/Images/knight.png')
player_front = pg.transform.scale(player_front, player_size)
player_right = pg.transform.flip(player_front, True, False)
player_rect = player_front.get_rect(topleft=(x, y))
current_player = player_front
facing = "left"

cat_size = (int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.071))
cat_img = pg.image.load("Pygame Implementations/Images/cat.png")
cat_img = pg.transform.scale(cat_img, cat_size)
cat_rect = cat_img.get_rect(topleft=(int(SCREEN_WIDTH*0.4), int(SCREEN_HEIGHT*0.5)))

TEXT_BOX_WIDTH = int(SCREEN_WIDTH * 0.8)   
TEXT_BOX_HEIGHT = int(SCREEN_HEIGHT * 0.2) 
text_rect = pg.Rect(int(SCREEN_WIDTH*0.1), int(SCREEN_HEIGHT*0.7), TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT)
line_height = int(SCREEN_HEIGHT * 0.03)
font_size = int(SCREEN_HEIGHT * 0.035)

def control_instructions(screen, instructions:str, font, color=(0,0,0)):
    full_instruction = "Press "+instructions+" to continue.."
    y_offset = int(SCREEN_HEIGHT * 0.02)
    text_surf = font.render(full_instruction, True, color)
    screen.blit(text_surf, (10, y_offset))
    
def generate_dialogue(player_choice=None, current_question=None):
    if player_choice is None:
        prompt = """
        You are an NPC in an RPG game. Ask the player a question in a friendly tone.
        Also, generate three short possible player responses.

        You must follow the following format while generating:
        Question: <text>
        Option1: <text>
        Option2: <text>
        Option3: <text>
        """
        
    else:
        prompt = f"""
        You are an NPC in an RPG game. 
        You had asked the following question: "{current_question}".
        The player just said: "{player_choice}".
        Respond appropriately and logically in a friendly tone in one short sentence.
        """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",  
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_dialogue(text: str):
    lines = text.strip().split("\n")
    question = lines[0].replace("Question:", "").strip()
    options = []
    for line in lines[1:]:
        _, option = line.split(":", 1)
        options.append(option.strip())
    return question, options

font = pg.font.SysFont('timesnewroman', font_size)

def draw_text(surface, text, color, rect, font, line_height):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        while font.size(word)[0] > rect.width:
            for i in range(1, len(word)+1):
                if font.size(word[:i])[0] > rect.width:
                    lines.append(current_line + word[:i-1])
                    word = word[i-1:]
                    break
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    y = rect.top
    max_y = rect.bottom
    for line in lines:
        if y + line_height > max_y:
            break
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (rect.left, y))
        y += line_height

def draw_dialogue(screen, question, options, step, npc_response=""):
    box_top = int(SCREEN_HEIGHT * 0.75)
    box_height = int(SCREEN_HEIGHT * 0.3)
    box = pg.Rect(int(SCREEN_WIDTH*0.05), box_top, int(SCREEN_WIDTH*0.9), box_height)

    pg.draw.rect(screen, (0,0,0), box)
    pg.draw.rect(screen, (255,255,255), box, 3)

    margin_x = int(SCREEN_WIDTH * 0.02)
    margin_y = int(SCREEN_HEIGHT * 0.02)
    effective_height = box.height - 2 * margin_y
    effective_width = box.width - 2 * margin_x

    if step == 0:
        num_lines = 1 + len(options)
        adaptive_line_height = min(int(SCREEN_HEIGHT*0.03), effective_height // num_lines)

        draw_text(screen, question, (255, 255, 255),
                  pg.Rect(box.left + margin_x, box.top + margin_y, effective_width, adaptive_line_height),
                  font, adaptive_line_height)

        option_start_y = box.top + margin_y + adaptive_line_height
        for i, opt in enumerate(options):
            opt_surface = font.render(f"{i+1}. {opt}", True, (200,200,200))
            opt_y = option_start_y + i * adaptive_line_height
            if opt_y + adaptive_line_height > box.bottom - margin_y:
                break
            screen.blit(opt_surface, (box.left + margin_x, opt_y))

    elif step == 1:
        words = npc_response.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] <= effective_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        max_lines = effective_height // int(SCREEN_HEIGHT*0.03)
        lines = lines[:max_lines]
        adaptive_line_height = effective_height // max(1, len(lines))

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (box.left + margin_x, box.top + margin_y + i * adaptive_line_height))


clock = pg.time.Clock()
npc_triggered = False
llm_called = False
conversation_step = 0
current_question = ""
can_move = True
player_choice_made = False

while True:    
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
            exit()

    keys = pg.key.get_pressed()
    if can_move:
        if keys[pg.K_a] and player_rect.x>0:
            player_rect.x-=speed
            current_player = player_front
            facing="left"
            # current_player = player_left
        elif keys[pg.K_d] and player_rect.x < SCREEN_WIDTH - player_rect.width:
            player_rect.x+=speed
            current_player = player_right
            facing = "right"
            # current_player=player_right
        elif keys[pg.K_w] and player_rect.y > 0:
            player_rect.y -= speed
            current_player = player_right if facing == "right" else player_front
            # current_player = player_back
        elif keys[pg.K_s] and player_rect.y < SCREEN_HEIGHT - player_rect.height:
            player_rect.y += speed
            current_player = player_right if facing == "right" else player_front
            # current_player = player_front
        # else:
            # current_player = player_front
    player_center = player_rect.center
    cat_center = cat_rect.center
    dx = player_center[0] - cat_center[0]
    dy = player_center[1] - cat_center[1]
    distance = (dx**2 + dy**2)**0.5
    npc_trigger_radius = int(SCREEN_WIDTH*0.04) 

    if distance<=npc_trigger_radius and conversation_step==0 and not llm_called:   

        if not npc_triggered:
            npc_triggered = True
            conversation_step = 0
            """ UNCOMMENT THE NEXT TWO LINES AND COMMENT THE 3 AFTER IT TO END DEBUGGING"""
            dialogue_text = generate_dialogue()
            current_question, options = parse_dialogue(dialogue_text)

            """COMMENT THE NEXT THREE LINES AND UNCOMMENT PREVIOUS TWO TO DEBUG """
            # dialogue_text = "llm called"
            # current_question = dialogue_text
            # options = ["Option 1", "Option 2", "Option 3"]

            llm_called = True
   
    if conversation_step == 0 and not npc_triggered:
        can_move = True
    else:
        can_move = False
    
    screen.fill((110, 200, 36))
    radius_rect = cat_rect.inflate(npc_trigger_radius*1.1, npc_trigger_radius*1.1)
    radius_surface = pg.Surface((radius_rect.width, radius_rect.height), pg.SRCALPHA)
    pg.draw.ellipse(radius_surface, (255, 0, 0, 50), radius_surface.get_rect())  
    screen.blit(radius_surface, radius_rect.topleft)
    screen.blit(current_player, player_rect.topleft)
    screen.blit(cat_img, cat_rect.topleft)
    

    if conversation_step == 0 and current_question and not player_choice_made:
        draw_dialogue(screen, current_question, options, step=0 )
        control_instructions(screen, "1, 2, 3", font, (0, 0, 255))
        if keys[pg.K_1]:
            player_choice = options[0]
            """ FOR DEBUGGING COMMENT/UNCOMMENT THE NEXT LINE """
            npc_response = generate_dialogue(player_choice, current_question)
            """ FOR DEBUGGING COMMENT/UNCOMMENT THE NEXT LINE """
            # npc_response = "response for opt1"
            conversation_step += 1
            player_choice_made = True
            
        elif keys[pg.K_2]:
            player_choice = options[1]
            """ FOR DEBUGGING COMMENT/UNCOMMENT THE NEXT LINE """
            npc_response = generate_dialogue(player_choice, current_question)
            """ FOR DEBUGGING COMMENT/UNCOMMENT THE NEXT LINE """
            # npc_response = "response for opt2"
            conversation_step += 1
            player_choice_made = True

        elif keys[pg.K_3]:
            player_choice = options[2]
            """ FOR DEBUGGING COMMENT/UNCOMMENT THE NEXT LINE """
            npc_response = generate_dialogue(player_choice, current_question)
            """ FOR DEBUGGING COMMENT/UNCOMMENT THE NEXT LINE """
            # npc_response = "response for opt3"
            conversation_step += 1
            player_choice_made = True
        
    if conversation_step==1:
        draw_dialogue(screen, current_question, options, step=1, npc_response=npc_response)
        control_instructions(screen, "SPACE", font, (0,0,255))
        if keys[pg.K_SPACE] or keys[pg.K_RETURN]:
            conversation_step = 0
            current_question = None
            npc_response = ""
            npc_triggered = False
            can_move = True
            player_choice_made = False
    pg.display.update()

    clock.tick(40)