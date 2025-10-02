import os
import json

root_path = os.getcwd()
character_path = os.path.join(root_path, 'Characters')
if not os.path.exists(character_path):
    os.makedirs(character_path)
    print("Added Characters folder.")

protagonist_info_file = 'protagonist_info.json'
protagonist_info_path = os.path.join(character_path, protagonist_info_file)


initial_data = {
    "name": "#",
    "role": "#",
    "appearance": {
        "age": "#",
        "gender": "#",
        "clothes": "#",
        "weapon": "#",
        "expression": "#"
    }
}

with open(protagonist_info_path, 'w') as f:
    json.dump(initial_data, f, indent=4)
print(f"Created initial Protagonist JSON file with blank values at {protagonist_info_path}")

with open(protagonist_info_path, 'r') as protagonist_file:
    protagonist = json.load(protagonist_file)

print("Lets customize your character!")
print("Enter the following details to make your character look as you want!")
print("If youre unable to think of anything, leave it blank.\n")

protagonist["name"] = input("What will you be liked to called as?: ")
protagonist["role"] = input("What role do you play? eg. a Knight, a Prince, a Wizard etc : ")

print("\nGreat, now lets define the appearance of your character.")
protagonist["appearance"]["age"] = input("The rough age of your character? : ")
protagonist["appearance"]["gender"] = input("Gender? : ")
protagonist["appearance"]["clothes"] = input("Describe the clothes or armour that the character is wearing: ")
protagonist["appearance"]["weapon"] = input("Any weapons you would like your character to carry?: ")

with open(protagonist_info_path, 'w') as protagonist_file:
    json.dump(protagonist, protagonist_file, indent=4)

print("Details of protagonist saved successfully.")
