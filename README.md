# Zombie Survival Game

A console-based survival game written in Python. Manage a squad of survivors — a Soldier, Medic, and Engineer — as you fight off increasingly dangerous zombies, heal your team, and build defenses.

---

## Installation Instructions

**Requirements:** Python 3 (no external libraries needed)

1. Download `Zombie_Survival_Game` and place it in a folder of your choice.
2. Open a terminal (Command Prompt or PowerShell on Windows).
3. Navigate to the folder containing the file:
   ```
   cd "C:\Users\YourName\Downloads"
   ```
4. Run the game:
   ```
   python option3_code_to_finish.py
   ```
   If that doesn't work, try:
   ```
   python3 option3_code_to_finish.py
   ```

---

## Controls

The game is menu-driven. Each turn, type the number for the action you want and press **Enter**.

| Input | Action |
|-------|--------|
| `1` | **Attack Zombie** — choose a survivor to deal damage to the zombie |
| `2` | **Heal** — choose a Medic and a target survivor to restore 20 HP |
| `3` | **Build Defense** — Engineer increases the squad's defense level by 5 |
| `4` | **Repair Weapon** — Engineer repairs a survivor's weapon durability |
| `5` | **Save Game** — save the current game state to a JSON file |
| `6` | **Load Game** — load a previously saved game from a JSON file |
| `7` | **Exit** — quit the game |

When prompted to select a survivor, type their **ID number** (shown in the status table) and press Enter.

---

## Features

### Squad Management
- Squad of four survivors: two Soldiers, one Medic, and one Engineer
- Each survivor has a name, current/max HP, a weapon, and a unique role
- Status table displayed each turn showing all survivor stats at a glance

### Combat System
- Player chooses a survivor to attack the zombie each turn
- After the player acts, the zombie counterattacks a random alive survivor
- Zombie damage is reduced by the squad's current defense level
- When the zombie dies, a new stronger zombie spawns and the day advances

### Survivor Abilities
- **Soldier** — no special ability; focused on high damage output
- **Medic** — heals a target survivor for 20 HP (max 3 uses per game)
- **Engineer** — builds defenses (+5 defense level) and repairs weapons (5 uses total)

### Weapon System
- Each weapon has a damage value and a durability rating
- Durability decreases by 1 with every attack
- Damage output is reduced when durability falls below 3
- A weapon with 0 durability is broken and cannot be used until repaired

### Save & Load System
- Save the full game state (squad stats, zombie stats, defense level, day) to a JSON file
- Load a saved game at any time to resume where you left off
- Default save file is `save.json` in the same folder as the script

### Error Handling
- Invalid menu inputs are caught and the menu is re-displayed
- Selecting a dead survivor for an action is blocked with a message
- Missing or corrupted save files are handled without crashing

---

## Optional Features Implemented

None at this time. Planned stretch goals for future versions include:

- Additional survivor roles (e.g., Scout with a dodge ability)
- Multiple zombie types with different behaviors
- A weapon/resource pickup system
- High score or survival day tracking across saves
