import os
from dotenv import load_dotenv
import json
import pixellab

load_dotenv()
PIXEL_KEY = os.getenv("PIXELLABKEY")

client = pixellab.Client(secret=PIXEL_KEY)

root_path = os.getcwd()
character_path = os.path.join(root_path, 'Characters')
protagonist_path = os.path.join(character_path, 'protagonist_info.json')

with open(protagonist_path, "r") as f:
    protagonist = json.load(f)

prompt_for_image = f"A {protagonist['appearance']['gender']} {protagonist['role']}, who is {protagonist['appearance']['age']} years old, wearing {protagonist['appearance']['clothes']} with a {protagonist['appearance']['weapon']}, their expression is {protagonist['appearance']['expression']}, light green background color. The character's entire body must be present in the image."

response = client.generate_image_pixflux(
    description=prompt_for_image,
    image_size=dict(width=128, height=128),
)
response.image.pil_image().save(os.path.join(character_path, "protagonist.png"))

print(f"Initial Protagonist Image saved at {os.path.join(character_path, "protagonist.png")}")