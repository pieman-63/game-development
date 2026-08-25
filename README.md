# Game Development

A personal journey into game development through learning, experimentation, and building actual projects.

This repository documents my transition from learning programming concepts to applying them in practical game-development projects. The goal is not only to learn how games are made, but to gradually develop the ability to design, build, test, and improve my own projects.

---

## Current Focus

My current focus is on **Python**, with **C++** planned as a future language to learn and explore.

At this stage, I consider myself a beginner/intermediate learner stepping into actual projects. This repository will therefore contain both experiments and progressively more structured projects as my skills develop.

---

# First Game Project

The first project is a **terminal-based RPG combat game** written in Python.

The project is designed as a practical introduction to:

- Object-oriented programming
- Character and enemy systems
- Combat mechanics
- Randomized enemy generation
- Player progression
- Experience and leveling
- Stat management
- Input handling
- Game-state management
- Procedural elements

The game currently runs entirely through the terminal and focuses on building a solid gameplay foundation before introducing more complex systems.

---

## Game Concept

The player creates a custom character by distributing a fixed number of stat points between four attributes:

- **Strength**
- **Defense**
- **Agility**
- **Intelligence**

The player then encounters dynamically generated enemies and must decide whether to:

1. Attack
2. Defend
3. Heal
4. Run

Defeating enemies rewards the player with EXP and can improve the character's statistics.

The gameplay continues until the player's HP reaches zero or the player chooses to quit.

---

## Character System

The game uses an object-oriented character hierarchy.

### Base Character

The `Character` class provides common functionality shared by the player and enemies.

Each character has:

- Name
- Strength
- Defense
- Agility
- Intelligence
- HP

Derived values are calculated automatically.

### Maximum HP

Maximum HP is determined by Defense:

```text
Max HP = 50 + (Defense × 5)
Developer: Tarun-coder1
