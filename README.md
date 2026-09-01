Game Development

A personal journey into game development through learning, experimentation, and building actual projects.

This repository documents my transition from learning programming concepts to applying them in practical game-development projects. The goal is not only to learn how games are made, but to gradually develop the ability to design, build, test, and improve my own projects.

---

Current Focus

My current focus is on Python, with C++ planned as a future language to learn and explore.

At this stage, I consider myself a beginner/intermediate learner stepping into actual projects. This repository therefore contains both experiments and progressively more structured projects as my skills develop.

---

Projects

1. Simple RPG Game

A terminal-based RPG combat game written in Python.

This project was my first major game-development project and serves as a practical introduction to designing a structured game using object-oriented programming.

Concepts explored

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

Game Concept

The player creates a custom character by distributing a fixed number of stat points between four attributes:

- Strength
- Defense
- Agility
- Intelligence

The player then encounters dynamically generated enemies and must decide whether to:

1. Attack
2. Defend
3. Heal
4. Run

Defeating enemies rewards the player with EXP and can improve the character's statistics.

The gameplay continues until the player's HP reaches zero or the player chooses to quit.

Character System

The game uses an object-oriented character hierarchy.

The "Character" class provides common functionality shared by the player and enemies.

Each character has:

- Name
- Strength
- Defense
- Agility
- Intelligence
- HP

Derived values are calculated automatically.

Maximum HP

Maximum HP is determined by Defense:

Max HP = 50 + (Defense × 5)

---

2. Guessing Game

A terminal-based number guessing game written in Python.

The game consists of multiple rounds where the player attempts to guess a randomly generated number between 1 and 100.

Features

- Three-round game sessions
- Random number generation
- Attempt tracking
- Progressive feedback based on how close the guess is
- Total attempt calculation
- Average attempts per game
- Score saving using CSV files

The game provides different levels of feedback depending on how far the player's guess is from the correct number, including messages such as:

- Much too low
- Much too high
- Low
- High

This project focuses on building familiarity with game loops, input validation, randomization, file handling, and basic score tracking.

---

3. Where's It in Pi?

A terminal-based Python game built around the digits of π (pi).

The game uses the first 10,000 digits of pi and challenges the player to identify where a randomly selected sequence of digits first appears.

Game Concept

The player is shown a sequence of digits taken from pi and must guess the 1-indexed position of its first occurrence within the stored digits.

The difficulty affects factors such as:

- Length of the digit sequence
- Guess tolerance
- Score multiplier
- Streak requirements

Features

- Local storage of pi digits
- Pi generation using the Chudnovsky algorithm
- Decimal precision handling
- Multiple difficulty levels
- Random digit sequence selection
- Position guessing mechanics
- Scoring system
- Difficulty-based multipliers
- Streak mechanics

This project explores more complex game mechanics while combining mathematical concepts, file handling, randomization, scoring systems, and precision-based calculations.

---

Repository Goals

As this repository grows, I plan to:

- Build more games and experiments
- Improve project structure and code organization
- Explore different gameplay mechanics
- Learn better object-oriented design
- Experiment with procedural systems
- Improve debugging and testing skills
- Eventually explore graphical game development
- Learn C++ and game-development concepts beyond Python

The projects in this repository represent my learning process, including experimentation, mistakes, refactoring, and gradual improvement.

---

Future Direction

This repository is intended to grow alongside my programming and game-development skills.

The current projects focus primarily on terminal-based games and gameplay logic. In the future, I plan to explore:

- Graphical interfaces
- Game engines
- More advanced AI systems
- Procedural generation
- Physics systems
- C++
- Larger and more complex game projects

---

Developer

pieman-63
