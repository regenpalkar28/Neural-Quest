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
    api_key=os.getenv("HF_TOKEN")
)

char_folder = "Characters"
if not os.path.exists(char_folder):
    os.makedirs(char_folder)


# ........... PROTAGONIST ....................................
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
# saving protagonist data in .json file
prot_json = json.loads(prot_data)
with open(protagonist_info_path, "w", encoding="utf-8") as f:
    json.dump(prot_json, f, indent=4)
print("Protagonist data saved. ")

# using protagonist data
with open(protagonist_info_path, "r", encoding="utf-8") as f:
    protagonist = json.load(f)
print("Protagonist's name: ", protagonist['name'])

# .............INITIAL STORYLINE BEFORE CHARACTER GENERATION .......................................

# creating the initial storyline
def prompt_for_initial_storyline(protagonist):
    return [
        f"{protagonist['name']}, {protagonist['role']}, starts their journey. "
        f"They appear {protagonist['appearance']['expression']}."
    ]

def initial_storyline(protagonist):
    prompt_for_storyline = f"""
    Generate an initial storyline on the genre "fantasy kingdom"

    use this information while generating:
    {prompt_for_initial_storyline(protagonist)[0]}
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

# -----------------------------CHARACTERS GENERATION--------------------------------------
characters_file = "characters.json"
char_info_path = os.path.join(char_folder, characters_file)

# creating characters
char_prompt = """
        Generate exactly 5 characters of the genre "fantasy kingdom".
        example characters can be A wise old man, a witch, a knight etc.
        Refer to this initial storyline too for generating characters:
        {story_text}
        Return ONLY a valid JSON array of 5 objects in the following format:

        [
        {
            "name": "<name>",
            "character_id": "<integer between 1 and 5 both inclusive>",
            "role": "<purpose of this character in the storyline>",
            "personality": "<gentle, aggressive, helpful>",
            "appearance": {
            "age": "<age of the character>",
            "gender": "<male or female if the character is human>",
            "expression": "<smiling, angry, worried, etc>",
            },
            
        }
        ]

        Important rules:
        - The role should not be "protagonist". All characters are NPC's
        - Replace all <...> with actual values.
        - Every value must be inside double quotes.
        - Do not include extra text, explanations, or code fences.
        """
print("Generating Characters...")
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
for char in characters:
    print(f"{char['character_id']}: {char['name']} ({char['role']})")
# --------------------STORYLINE GENERATION & UPDATION--------------------------------------

def storyline_updater(protagonist, story, missions, characters, completed_missions):
    # if no more npcs are left then: 
    if completed_missions >= len(characters):
        return missions, story, completed_missions
    
    # here we assume that solved characters already has some data
    npc = characters[completed_missions]
    next_npc = characters[completed_missions+1] if completed_missions + 1 < len(characters) else None
    
    mission_obj = mission(protagonist, npc, story, next_npc)
    missions.append(mission_obj)

    new_context = mission_obj["expanded_story"]
    with open(storyline_file, "a", encoding="utf-8") as f:
        f.write("\n" + new_context)

    return missions, new_context, completed_missions+1

# ---------------------- MISSIONS -------------------------------
missions_file = "missions.json"
missions = []
with open(storyline_file, "r", encoding="utf-8") as f:
    story_text = f.read()

previous_context_mission = story_text

def mission_prompt_generator(protagonist, NPC, context=None):
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
    # Generate base mission structure
    mission_obj = mission_prompt_generator(protagonist, NPC, context)
    # Converting mission to a string for LLM
    mission_text = f"Title: {mission_obj['mission_title']}\nDescription: {mission_obj['mission_description']}"
    next_name = next_NPC["name"] if next_NPC else "the journey ahead"
    mission_prompt = f"""
        Expand the following mission for a fantasy kingdom story.
        Include events, challenges, dialogue, or any interesting twists:

        {mission_text}
        Also make sure that the mission somehow leads the protagonist towards {next_name}.
        """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": mission_prompt}]
    )
    expanded_story = response.choices[0].message.content
    
    return {
        "mission_title": mission_obj['mission_title'],
        "mission_description": mission_obj['mission_description'],
        "expanded_story": expanded_story
    }

# ---- simulating the protagonist meeting NPCs one by one -------------

current_npc_idx = 0
completed_missions = 0
missions = []

with open(storyline_file, "r", encoding="utf-8") as f:
    story_text = f.read()

context = story_text

while completed_missions < len(characters):
    npc = characters[completed_missions]
    print(f"\n--- Mission {completed_missions + 1} ---")
    print(f"Meeting NPC: {characters[completed_missions]['name']}")
    missions, context, completed_missions = storyline_updater(
        protagonist, context, missions, characters, completed_missions
    )
    print("Mission title:", missions[-1]['mission_title'])
    
