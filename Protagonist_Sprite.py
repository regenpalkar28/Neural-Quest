import os
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
from huggingface_hub import login
import json
import torch

# from huggingface_hub import InferenceClient
# load_dotenv()
# hf_token = os.getenv("HF_TOKEN")
# login(hf_token)
# client = InferenceClient(
#     provider="nebius",
#     api_key=hf_token,
# )
#  1 image took 10% of my Inference credits, so the commented part will not be used.

device = 'cuda' if torch.cuda.is_available() else 'cpu'

root_path = os.getcwd()
character_path = os.path.join(root_path, 'Characters')
protagonist_path = os.path.join(character_path, 'protagonist_info.json')

image_model_path = os.path.join(root_path, "aziibpixelmix_v10.safetensors")

with open(protagonist_path, "r") as f:
    protagonist = json.load(f)

prompt_for_image = f"A {protagonist["appearance"]["gender"]} {protagonist["role"]}, who is {protagonist["appearance"]["age"]} years old, wearing {protagonist["appearance"]["clothes"]} with a {protagonist["appearance"]["weapon"]}, their expression is {protagonist["appearance"]["expression"]}, white background. The character's entire body must be present in the image."

pipe =  StableDiffusionPipeline.from_single_file(image_model_path).to(device)

image = pipe(prompt_for_image, guidance_scale =7.5,num_inference_steps=20, height = 512, width = 512).images[0]

image.save(os.path.join(character_path, "protagonist.png"))
print(f"Initial Protagonist Image saved at {os.path.join(character_path, "protagonist.png")}")