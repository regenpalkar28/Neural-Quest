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

root_path = os.getcwd()
character_path = os.path.join(root_path, 'Characters')

protagonist_info_path = os.path.join(character_path, 'protagonist_info.json')

with open(protagonist_info_path, "r") as f:
    prot_data = json.load(f)

json_template = """
    {
    "name": "<name>",
    "role": "<role of the protagonist in the story, such as a fighter, an explorer>",
    "appearance": {
        "age": "<age>",
        "gender": "<male or female>",
        "clothes": "<what clothing the protagonist is wearing. If the protagonist is wearing armour, then armor instead of clothes>",
        "weapon": "<what kind of weapon is used>",
        "expression": "<expression, e.g., determined, serious, etc.>"
    },
}
"""
prompt_for_protagonist = f"""
Complete the following JSON data for a protagonist.
For any value marked with a '#', generate a creative and fitting description.
For clothes, weapons and expression, dont make it too elaborative,just structure and describe it properly, and only use adjectives.
For example, instead of "weapons":"He possesses a katana forged in the deepest pits of fire..", just describe the weapon.
Make sure the output is a valid JSON object. Do not add any random text before or after it.

Input JSON:
{{
    "name": "{prot_data["name"]}",
    "role": "{prot_data["role"]}",
    "appearance": {{
        "age": "{prot_data["appearance"]["age"]}",
        "gender": "{prot_data["appearance"]["gender"]}",
        "clothes": "{prot_data["appearance"]["clothes"]}",
        "weapon": "{prot_data["appearance"]["weapon"]}",
        "expression": "{prot_data["appearance"]["expression"]}"
    }}
}}

Make sure the output is of the form
{json_template}

output only the json.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b:cerebras",
    messages=[{"role": "user", "content": prompt_for_protagonist}]
    )

prot_data_temp = response.choices[0].message.content
prot_data_updated = json.loads(prot_data_temp)

with open(protagonist_info_path, "w") as f:
    json.dump(prot_data_updated,f,indent=4)

print("Protagonist Info cleaned using LLM.")
print(f"Updated Protagonist Info saved at {protagonist_info_path}")


