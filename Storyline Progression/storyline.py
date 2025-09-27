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

char_folder = "Characters"
if not os.path.exists(char_folder):
    os.makedirs(char_folder)

character_num = 5
#PROTAGONIST INFO
protagonist_file = "protagonist.json"
protagonist_info_path = os.path.join(char_folder, protagonist_file)
prot_prompt = """
    Generate a protagonist character for a story which is of the genre "fantasy kingdoms".
    Output in JSON format like this:

{
    "name": "<name>",
    "role": "<role of the protagonist in the story, such as a fighter, an explorer>",
    "appearance": {
        "age": "<age>",
        "gender": "<male or female>",
        "clothes": "<what clothing the protagonist is wearing. If the protagonist is wearing armour, then armor instead of clothes>",
        "weapon": "<what kind of weapon is used>",
        "expression": "<expression, e.g., determined, serious, etc.>",
    },

}
All values in double quotes. Output ONLY the JSON object.
"""
prot_response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",  
        messages=[{"role": "user", "content": prot_prompt}]
    )
prot_data = prot_response.choices[0].message.content
print("Protagonist data generated.")
#saving protagonist data in .json file
prot_json = json.loads(prot_data)
with open(protagonist_info_path, "w", encoding="utf-8") as f:
    json.dump(prot_json, f, indent=4)
print("Protagonist data saved. ")

#using protagonist data
with open(protagonist_info_path, "r", encoding="utf-8") as f:
    protagonist = json.load(f)
# print("Protagonist's name: ", protagonist['name'])

#INITIAL STORYLINE BEFORE CHARACTER GENERATION

def initial_storyline(protagonist):
    prompt_for_storyline = f"""
    Generate an initial storyline on the genre "fantasy kingdom"
    
    use this information while generating:
    {[
        f"{protagonist['name']}, {protagonist['role']}, starts their journey. "
        f"They appear {protagonist['appearance']['expression']}."
    ]}
    Important rules:
        - Do not create ANY NPCs. This initial storyline must only have the protagonist who has just started his/her adventure
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
with open(storyline_file, "r", encoding="utf-8") as f:
    story_text = f.read()

# CHARACTERS GENERATION
characters_file = "characters.json"
char_info_path = os.path.join(char_folder, characters_file)

# creating characters
characterprompt_json_format = """
    [
        {
            "name": "<name>",
            "character_id": "<integer between 1 and 5 both inclusive>",
            "role": "<purpose of this character in the storyline>",
            "personality": "<gentle, aggressive, helpful>",
            "appearance": {
            "age": "<age of the character>",
            "gender": "<male or female if the character is human>",
            "expression": "<smiling, angry, worried, etc>"
            },
            
        }
        ]

        Important rules:
        - The role should not be "protagonist". All characters are NPC's
        - Replace all <...> with actual values.
        - Every value must be inside double quotes.
        - Do not include extra text, explanations, or code fences.
    """
# creating characters
char_prompt = f"""
        Generate exactly {character_num} characters of the genre "fantasy kingdom".
        example characters can be A wise old man, a witch, a knight etc.
        Refer to this initial storyline too for generating characters:
        {story_text}
        Return ONLY a valid JSON array of 5 objects in the following format:

        {characterprompt_json_format}
        """
print("generating characters...")
char_response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",  
        messages=[{"role": "user", "content": char_prompt}]
    )
character_data = char_response.choices[0].message.content

# saving character data in .json file
character_json = json.loads(character_data)
with open(char_info_path, "w", encoding="utf-8") as f:
    json.dump(character_json, f, indent=4)
print("Character data saved.")

# using stored data
with open(char_info_path, "r", encoding="utf-8") as f:
    characters = json.load(f)

# STORYLINE GENERATION & UPDATION
def storyline_updater(protagonist, mission, NPC):
    content = f"""
    The following mission has been completed, after {protagonist["name"]} meets {NPC["name"]}, who is a {NPC["role"]}:
    {mission["expanded_story"]}
    """
    with open('story.txt', 'a', encoding="utf-8") as f:
        f.write(content)

# MISSIONS

with open(storyline_file, "r", encoding="utf-8") as f:
    story_text = f.read()

previous_context_mission = story_text

def mission_prompt_constructor(protagonist, NPC, context=None):
    description = ""
    if context:
            description+=f"{context} Then, {protagonist['name']} encounters {NPC['name']} ({NPC['role']}). "
            description+=(
                f"Their interaction mixes the protagonist with {NPC['personality']}, "
                f"creating tension and a challenge."
                )
    return {
        "mission_title": f"{protagonist['name']} meets {NPC['name']}",
        "mission_description": description
    }

def mission(protagonist, NPC, context, next_NPC=None):
    mission_obj = mission_prompt_constructor(protagonist, NPC, context)
    # has mission_title and mission_description

    # Converting mission to a string for LLM
    mission_text = f"Title: {mission_obj['mission_title']}\nDescription: {mission_obj['mission_description']}"
    if next_NPC:
        mission_prompt = f"""
            Generate the following mission for a fantasy kingdom story.
            Include events, challenges, dialogue, or any interesting twists:

            {mission_text}
            Also make sure that the mission somehow leads the protagonist towards {next_NPC["name"]}.
            """
    else:
        mission_prompt = f"""
            Generate the following mission for a fantasy kingdom story.
            Include events, challenges, dialogue, or any interesting twists:

            {mission_text}
            \n This is the final mission.
            """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": mission_prompt}]
    )
    mission_story = response.choices[0].message.content
    
    return {
        "mission_title": mission_obj['mission_title'],
        "mission_description": mission_obj['mission_description'],
        "expanded_story": mission_story
    }

missions=[]
for char_idx in range(character_num-1):
    missions.append(mission(protagonist, characters[char_idx], story_text, characters[char_idx+1]))
    storyline_updater(protagonist, missions[char_idx], characters[char_idx])
# for the last character
missions.append(mission(protagonist, characters[character_num-1], story_text))
storyline_updater(protagonist, missions[character_num-1], characters[character_num-1])
    
