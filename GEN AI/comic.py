from dotenv import load_dotenv
from langchain_community.llms import Ollama
from diffusers import StableDiffusionPipeline
import torch
import cv2
import numpy as np

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

load_dotenv()

llm = Ollama(model="gemma:2b")

n = int(input("Welcome to comics generator, please enter the number of characters that you want: "))
characters = []
dialogues = []
print(f"Please Input characteristics and dialogues of the {n} characters below.\n")
print("Characteristics can be complexion, color of clothes, any items that characters are holding, etc. Make sure to add as much detail as possible for an accurate result. \n")
for i in range(n):
    char = input(f"Please enter characteristics of character {i+1}: \n")
    dialogue = input(f"Please input some dialogues that you want this character to say: \n")
    characters.append(char)
    dialogues.append(dialogue)

prompt_to_LLM = f"You are supposed to generate a prompt for an image generation model, which is being used to generate an image of a comic. The comic should have three panels, and it involves {n} characters."

for i in range(n):
    prompt_to_LLM+= f"Character {i+1}: Characteristics: {characters[i]}; Dialogues: {dialogues[i]}. "
prompt_to_LLM+= "Create a creative and a visually descriptive prompt for an image generation model to generate a comic strip."

prompt_to_ImageModel = llm.invoke(prompt_to_LLM)
image = pipe(prompt_to_ImageModel).images[0]
image_np = np.array(image)[:, :, ::-1]
cv2.imshow(image_np)