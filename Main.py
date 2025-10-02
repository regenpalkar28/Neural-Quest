import os
import sys
import subprocess

venv_python = os.path.join(sys.prefix, 'Scripts', 'python.exe')

print("Generating World..")
subprocess.run([venv_python, 'world_generator.py'], check=True)
print("World Generated")

print("\nTaking User Input for Protagonist..")
subprocess.run([venv_python, 'Protagonist_User_Input.py'], check=True)

print("\nCleaning and completing Information..")
subprocess.run([venv_python, 'Prot_Info_Complete.py'], check=True)

print("\nGenerating Sprite for character...")
subprocess.run([venv_python, 'Protagonist_Sprite.py'], check=True)

