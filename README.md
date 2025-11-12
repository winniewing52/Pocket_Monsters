# 🎮 Pocket Monsters 🎮
A Python implementation of a Pokemon Battle game system where trainers can assemble teams, battle other trainers, and progress through a Battle Tower gauntlet.

## 📝 Overview
This project stimulates the classic Pokémon battle system featuring:
* 70+ Pokémon types with unique starts and evolution chains
* Multiple battle modes
* Type effectiveness system with strategic combat mechanics
* Battle Tower - A gauntlet mode where players face multiple trainers
* Pokédex tracking system that influences battle outcomes

## Key Features ✨
**Core Systems**
* **Type Effectiveness**: Rock-paper-scissors style combat us8ing a CSV-based effectiveness table
* **Evolution System**: Pokémon evolve when leveling up, with stat multipliers
* **Experience and Leveling**: Pokémon gain experience from battles and levelup
* **Trainer System**: Trainers manage teams and track Pokédex completion

**Battle Modes**
* **Set Mode**: "King of the Hill" - One Pokémon fights until defeated
* **Rotating Mode**: Pokémon cycle to the back after each turn
* **Optimised Mode**: Team ordered by custom criterion (HP, Attack, Defense, Speed, Level)

**Advanced Features**
* **Speed-based turn order**: Faster Pokémon attack first
* **Simultaneous attacks**: When speeds are equal
* **Pokédex multiplier**: Experienced trainers deal more damage
* **Special moves**: Mode-specific team manipulations
* **Battle Tower**: Multi-trainer gauntlet with lives system