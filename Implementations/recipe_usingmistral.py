import os
from openai import OpenAI
from dotenv import load_dotenv
from huggingface_hub import login
import time

load_dotenv()
token = os.getenv("HF_TOKEN")
login(token)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)
print("Hey, welcome to this recipe generator, We will help you create the perfect dish based on your preferences and what materials you have available.")
cuisine = input("Do you wish to have a recipe from a particular cuisine? (such as Indian, Chinese, Italian etc) : ")
ingredients = input("What ingredients do you have available? (such as chicken, potatoes, etc): ")
filt = input("Do you wish to apply any filters? (such as vegetarian, vegan, gluten free, or any allergies): ")

prompt = f"Show me a recipes for a dish in the cuisine {cuisine} with the following ingredients: {ingredients}. List all the ingredients used in the recipe, the recipe should adhere to the following filter {filt} : "

tic = time.time()
completion = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
)
toc = time.time()
print(completion.choices[0].message)
print(f"Time taken to generate: {toc-tic}s")
