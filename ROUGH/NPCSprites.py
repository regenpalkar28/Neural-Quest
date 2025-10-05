import os
from dotenv import load_dotenv
import json
import pixellab
import NPC_info

load_dotenv()
PIXEL_KEY = os.getenv("PIXELLABKEY")

client = pixellab.Client(secret=PIXEL_KEY)
character_path = os.path.join(os.getcwd(), 'Characters')

NPC_path = os.path.join(character_path, 'NPC.json')

with open(NPC_path, "r") as f:
    NPC_data = json.load(f)

char_num = NPC_info.character_num
count = 1

for NPC in NPC_data:
    gender = NPC['appearance']['gender']
    role = NPC['role']
    age = NPC['appearance']['age']
    clothes = NPC['appearance']['clothes']
    weapon = NPC['appearance']['weapon']
    expression = NPC['appearance']['expression']

    prompt_for_image = f"A {gender} {role}, who is {age} years old, wearing {clothes} holding a {weapon}, their expression is {expression}, light green background color. The character's entire body must be present in the image."

    response = client.generate_image_pixflux(
    description=prompt_for_image,
    image_size=dict(width=128, height=128),
    )
    response.image.pil_image().save(os.path.join(character_path, f"NPC_{count}.png"))
    print(f"Image for NPC {count} saved at {os.path.join(character_path, f"NPC_{count}.png")}")
    count = count + 1
