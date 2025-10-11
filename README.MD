<a href="https://github.com/regenpalkar28/Neural-Quest">
<h1 align = "center"> <strong> AI Dungeon Master</strong></h1>

<h3 align = "center">

</p>
  RPG Simulator AI Dungeon master 

</h3>

</div>
<hr>

<details>
<summary>Table of Contents</summary>

- [Description](#description)
- [Main Parts of Project](#Main part of project)
- [Phases for World Generation](#phases)
- [ Ocean Formation Logic](#Ocean Formation Logic)
- [Links](#links)
- [Tech Stack](#tech-stack)
- [Progress](#progress)
- [Future Scope](#future-scope)
- [Applications](#applications)
- [Project Setup](#project-setup)
- [Usage](#usage)
- [Team Members](#team-members)
- [Mentors](#mentors)
- [Screenshots](#screenshots)
- [Contributor's Guidelines](#how-to-contribute)

</details>
<hr>




📝Description

This project is an AI-powered interactive fantasy RPG game . Players control a protagonist exploring a procedurally generated world filled with NPCs, obstacles, and quests. Each NPC encounter dynamically generates dialogues and story events using LLM  model, creating a unique and evolving narrative for every playthrough. The game combines procedural world generation, modular NPC design, and AI-driven storytelling to provide an immersive and personalized RPG experience."

Key Features:

1]   Dynamic AI  Storytelling  : NPC dialogues and story events are generated in real time using AI. This means every encounter is unique, and the storyline evolves differently in each playthrough.

2]   Procedurally Generated World: The game world is automatically created with different terrains, obstacles, and spawn points. This ensures that no two game sessions are exactly the same, keeping the experience fresh.

3]   Interactive NPCs: NPCs have distinct personalities and roles, guiding the player through missions and story events. They respond dynamically depending on the player’s actions and location in the world.


Main Parts of Project

-Procedural world generation

The world generation system creates procedurally generated island environments using Perlin Noise with radial falloff. Each generated world is a unique 12,000×12,000 pixel island with 7 distinct terrain types, ensuring no two playthroughs are identical.
Key Features

- Procedural Generation:  Uses multi-octave Perlin noise for natural terrain

- Island Formation: Circular falloff creates realistic island geography

-7 Terrain Types: From deep ocean to mountain peaks

- Multiple Output Formats: Terrain IDs, colored maps, and tiled artwork

Efficient Storage: Tile-based generation with upscaling
Deterministic: Can reproduce worlds with same random seed


Phases for World Generation:

Phase 1: Initialization. Set world parameters (size, tile count, noise scale)
        - Create empty arrays for noise and terrain data        │
        - Initialize gradient grid (201×201 random vectors)  

Phase 2: For each tile (200×200 grid):                          │
       - We will  Calculate base Perlin noise                        
        - Apply octave layering (5 layers)   
        - Normalize values to [0, 1]                       
        - Store in noise_map array

Phase 3: Island formation
      - For each tile:    
      -  we calculate first where is center of world located
      -  We willCalculate distance from world center  and find  falloff  Compute falloff: max(0, 1 - distance)              │
      -  Apply falloff: final = noise × falloff             │
      -  Result: Higher terrain at center, ocean at edges


🌊 Ocean Formation Logic

The ocean regions in the generated world are formed through a combination of Perlin noise and a radial falloff function.
Perlin noise first generates smooth elevation values between 0 (low) and 1 (high), representing the natural terrain height variations such as plains, hills, and mountains.
To ensure that the world has a central landmass surrounded by ocean boundaries, a falloff factor is applied based on the distance of each point from the map center.
This value gradually decreases towards the edges, effectively reducing the terrain height near corners and edges.

After this adjustment, the normalized height map is classified into terrain types (e.g., ocean, sand, grass, rock, snow) using threshold values.

Points with very low height values (typically < 0.05) are marked as ocean, creating smooth and realistic coastlines around the land area.

As a result, the generated map naturally evolves into an island-like world, where the central region features elevated land and the outer boundaries transition into deep ocean — mimicking real-world geographical formations.



## 🔗Links

- [GitHub Repository](https://github.com/regenpalkar28/Neural-quest)
- [Demo Video]()
- [Drive Link to Screenshots of your project]()




## 📈Progress

- [x] Procedural world with varied terrains and obstacles is implemented.
-  [x]  Player movement, collision detection, and camera follow are functional.
-  [x] NPCs spawn dynamically with unique roles, personalities, and appearances.
- [x] AI generates dialogues and story events in real time.


## 🔮Future Scope


 -  Multiplayer mode
-   Adaptive music sounds
-   Branching NPC quests
-   Larger game world

## 💸Applications
This project comes under the Generative AI category and contributes to research in AI-driven interactive storytelling and gaming. The main applications of this project are:

-  Research in Generative AI – Explores AI for real-time story and dialogue generation.
-  Interactive Character Design
-  Immersive Gameplay Experiences

## 👨‍💻Team Members

- [Bhavika Wankhede](https://github.com/bhavika21-ux): 
- [Regen Palkar](https://github.com/regenpalkar28): 
- 

## 👨‍🏫Mentors

- [Vidhhi Rohira](https://github.com/vidhirohira):
- [Aadit Pujari](







