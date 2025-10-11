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

character_num = 5
character_folder = os.path.join(os.getcwd(), 'Characters')
char_info_path = os.path.join(character_folder, 'NPC.json')

storyline_file = "story.txt"
with open(storyline_file, "r", encoding="utf-8") as f:
    story_text = f.read()

NPC_json_format = """
    [
        {
            "name": "<name>",
            "role": "<purpose of this character in the storyline>",
            "personality": "<gentle, aggressive, helpful>",
            "appearance": {
                "age": "<age of the character>",
                "gender": "<male or female if the character is human>",
                "clothes": "<what clothing the protagonist is wearing. If the protagonist is wearing armour, then armor instead of clothes>",
                "weapon": "<what kind of weapon is used>",
                "expression": "<smiling, angry, worried, etc>"
            },
            
        }
        ]

        Important rules:
        - The role should not be "protagonist". All characters are NPC's
        - Replace all <...> with actual values.
        - Every value must be inside double quotes.
        - Do not include extra text, explanations, or code.
    """

char_prompt = f"""
        Generate exactly {character_num} characters of the genre "fantasy kingdom".
        example characters can be A wise old man, a witch, a knight etc.
        Refer to this initial storyline too for generating characters:
        All the characters are on an island.
        {story_text}
        Return ONLY a valid JSON array of 5 objects in the following format:

        {NPC_json_format}
        """
response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",  
        messages=[{"role": "user", "content": char_prompt}]
    )
character_data = response.choices[0].message.content

# saving character data in .json file
character_json = json.loads(character_data)
with open(char_info_path, "w", encoding="utf-8") as f:
    json.dump(character_json, f, indent=4)
print(f"Character data saved at {char_info_path}.")

