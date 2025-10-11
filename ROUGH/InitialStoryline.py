import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from huggingface_hub import login

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
login(hf_token)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token
)

character_folder = os.path.join(os.getcwd(), 'Characters')
protagonist_json = os.path.join(character_folder, 'protagonist_info.json')

with open(protagonist_json, "r", encoding="utf-8") as f:
    protagonist = json.load(f)

def initial_storyline(protagonist):
    prompt_for_storyline = f"""
    Generate an initial storyline on the genre "fantasy kingdom"
    
    use this information while generating:
    {f"{protagonist['name']}, a {protagonist['role']}, starts their journey on an island. "}
    {f"They appear {protagonist['appearance']['expression']}."}
    
    Important rules:
        - Do not create ANY NPCs or characters other than the protagonist. This initial storyline must only have the protagonist who has just started his/her adventure
        - Keep the initial storyline short, less than 40 words.
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",  
        messages=[{"role": "user", "content": prompt_for_storyline}]
    )
    storyline = response.choices[0].message.content
    return storyline

storyline_file = "story.txt"
with open(storyline_file, "w", encoding="utf-8") as f:
    f.write(initial_storyline(protagonist)) 
print("initial storyline generated.")
