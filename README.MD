# 🧙‍♂️ AI Dungeon Master

### 🎮 RPG Simulator — AI-Powered Dungeon Master

---

## Table of Contents
- [Description](#description)
- [Main Parts of Project](#main-parts-of-project)
- [Phases for World Generation](#phases-for-world-generation)
- [Ocean Formation Logic](#ocean-formation-logic)
- [Image Generation of Characters and NPCs](#image-generation-of-characters-and-npcs)
- [LLM Storytelling System](#llm-storytelling-system)
- [Links](#links)
- [Tech Stack](#tech-stack)
- [Progress](#progress)
- [Future Scope](#future-scope)
- [Applications](#applications)
- [Project Setup](#project-setup)
- [Team Members](#team-members)
- [Mentors](#mentors)
- [Screenshots](#screenshots)
- [Contributor's Guidelines](#contributors-guidelines)

---

## Description

**AI Dungeon Master** is an **AI-powered interactive fantasy RPG**.  
Players control a protagonist exploring a **procedurally generated world** filled with NPCs, obstacles, and quests.  
Each NPC encounter dynamically generates dialogues and story events using a **pretrained LLM**, creating a **unique and evolving narrative** for every playthrough.

This project combines **procedural world generation**, **modular NPC design**, and **AI-driven storytelling** to deliver an **immersive RPG experience**.

---

### Key Features

1. **Dynamic AI Storytelling** — NPC dialogues and story events are generated in real-time using AI, ensuring every encounter is unique.  
2. **Procedurally Generated World** — Automatically creates diverse terrains, obstacles, and spawn points, ensuring no two worlds are identical.  
3. **Interactive NPCs** — NPCs have distinct personalities and dynamically respond to the player's actions and position in the world.

---

## Main Parts of Project

### Procedural World Generation

The world generation system creates **procedurally generated island environments** using **multi-octave Perlin Noise** combined with **radial falloff**.

Each world is a unique **12,000 × 12,000 px** island with **7 terrain types**, ensuring no two playthroughs are identical.

#### Key Features
- **Procedural Generation:** Multi-octave Perlin noise for natural terrain  
- **Island Formation:** Circular falloff for realistic island geography  
- **7 Terrain Types:** From deep ocean to snowy mountain peaks  
- **Multiple Output Formats:** Terrain IDs, colored maps, and tiled artwork  
- **Efficient Storage:** Tile-based generation with upscaling  
- **Deterministic:** Same seed → same world  

---

## Phases for World Generation

### Phase 1 — Initialization
- Set world parameters (size, tile count, noise scale)  
- Create empty arrays for noise and terrain data  
- Initialize gradient grid (201×201 random vectors)

### Phase 2 — Noise Calculation
For each tile (200×200 grid):  
- Calculate base Perlin noise  
- Apply octave layering (5 layers)  
- Normalize values to `[0, 1]`  
- Store results in `noise_map` array  

### Phase 3 — Island Formation
For each tile:  
- Calculate distance from world center  
- Compute falloff: `max(0, 1 - distance)`  
- Apply falloff: `final_height = noise × falloff`  
- Result: Higher terrain near center, ocean at edges  

---

## Ocean Formation Logic

Ocean regions are generated through **Perlin noise + radial falloff** combination.

1. **Base Terrain (Perlin Noise):** Produces elevation values between `0.0` (low) and `1.0` (high), creating smooth terrain variations such as plains, hills, and mountains.

2. **Radial Falloff Application:** Distance from the center determines terrain suppression near edges. Falloff gradually decreases elevation values toward the corners to form coastlines.

3. **Terrain Classification:** Based on final height:
- `< 0.05 → Deep Ocean `
- `0.05–0.15 → Beach `
- `0.15–0.35 → Grasslands `
- `0.35–0.55 → Hills `
- `> 0.55 → Snow Peaks `
  
The ocean regions in the generated world are formed through a combination of Perlin noise and a radial falloff function. Perlin noise first generates smooth elevation values between 0 (low) and 1 (high), representing the natural terrain height variations such as plains, hills, and mountains. To ensure that the world has a central landmass surrounded by ocean boundaries, a falloff factor is applied based on the distance of each point from the map center. This value gradually decreases towards the edges, effectively reducing the terrain height near corners and edges.

After this adjustment, the normalized height map is classified into terrain types (e.g., ocean, sand, grass, rock, snow) using threshold values.

Points with very low height values (typically < 0.05) are marked as ocean, creating smooth and realistic coastlines around the land area.

As a result, the generated map naturally evolves into an island-like world, where the central region features elevated land and the outer boundaries transition into deep ocean — mimicking real-world geographical formations.
This combination naturally forms an **island with central land and ocean boundaries**, mimicking real-world geography.

---

## Image Generation of Characters and NPCs

All information about **NPCs** and the **protagonist** is stored in a **JSON file**, including:
- **Name**
- **Role**
- **Personality**
- **Location or region**
- **Quest relevance**

This file acts as the **central knowledge base** for character creation and story logic.

### NPC Image Generation Logic

1. **Data Extraction:** Read each NPC’s attributes from JSON and create a **prompt for image generation**.  
2. **Sequential Generation (NPC Sequence):** Images are generated in a defined sequence (`NPC_sequence`) to ensure storyline consistency.  
3. **Background Removal:** Remove background pixels to produce clean, transparent sprites suitable for in-game rendering.  
4. **Storage:** All character images are stored in the `character_path` folder for use in the game.

---

## LLM Storytelling System

### Dynamic Dialogue Generation

When the **protagonist collides with an NPC**, a **dialogue sequence** is triggered. The **LLM** generates context-aware dialogues and narrative events based on:
- NPC’s personality and role  
- Current world region  
- Active quest or storyline stage

### Storyline Generation and Progression

1. **Correct NPC Interaction:** Advances story, generates quests or discoveries.  
   Example:  
   > “As the sun dips below the horizon, the old sage gestures toward the northern ruins — a new journey begins.”

2. **Wrong NPC Interaction:** Triggers fallback dialogue:  
   > “I can’t talk right now…”  
   Guides the player to the correct NPC.

3. **Simultaneous Story + Dialogue Display:** Both dialogue text and story narration appear on screen to create a **cinematic effect**.

4. **Dynamic Quest Flow:** NPC interactions update protagonist objectives, NPC relationships, and world state.

---

##  Links

- [GitHub Repository](https://github.com/regenpalkar28/Neural-Quest)  
- [Demo Video]()  
- [Drive Link for Screenshots]()

---

##  Tech Stack
- **Python** — Core logic and simulation  
- **Pygame** — Rendering, player movement, collision detection  
- **NumPy** — Procedural terrain calculations  
- **Perlin Noise** — Terrain generation  
- **PIL (Python Imaging Library)** — Image generation and processing  
- **LLM Model** — Dynamic dialogue & story generation  

---

## Progress
- [x] Procedural terrain & obstacle generation  
- [x] Player movement, collision detection, camera follow  
- [x] Dynamic NPC spawning with unique personalities  
- [x] Real-time AI dialogue and story event generation  

---

##  Future Scope
- Multiplayer world exploration  
- Adaptive music and ambient sound  
- Branching questlines from NPCs  
- Larger open-world expansion  

---

##  Applications
This project falls under **Generative AI** and contributes to **AI-driven interactive storytelling** and **game world generation**.

**Main Applications:**  
- Research in Generative AI — Real-time story and dialogue generation  
- Interactive Character Design  
- Immersive Gameplay Experiences  

---
---

## Team Members

- [Bhavika Wankhede](https://github.com/bhavika21-ux): 
- [Regen Palkar](https://github.com/regenpalkar28): 
- 

## Mentors

- [Vidhhi Rohira](https://github.com/vidhirohira):
- [Aadit Pujari](https://github.com/pipinstallaadit):

---

##  Project Setup
```bash
# Clone the repository
git clone https://github.com/regenpalkar28/Neural-Quest.git

# Navigate into project folder
cd Neural-Quest

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py

---








