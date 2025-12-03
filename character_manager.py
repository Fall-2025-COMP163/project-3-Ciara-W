"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module
Name: [Your Name Here]
AI Usage: [Document any AI assistance used]

This module handles character creation, loading, saving, and character management.
"""

import os

from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    CharacterDeadError,
    InvalidSaveDataError,
    SaveFileCorruptedError
)

# ======================================================================
# CHARACTER CREATION
# ======================================================================

def create_character(name, character_class):
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    stats = valid_classes[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

# ======================================================================
# CHARACTER EXPERIENCE & LEVELING
# ======================================================================

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead")

    character["experience"] += xp_amount

    while True:
        required = character["level"] * 100
        if character["experience"] >= required:
            character["experience"] -= required
            character["level"] += 1
            character["max_health"] += 10
            character["strength"] += 2
            character["magic"] += 2
            character["health"] = character["max_health"]
        else:
            break

# ======================================================================
# GOLD MANAGEMENT
# ======================================================================

def add_gold(character, amount):
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative")
    character["gold"] = new_total
    return character["gold"]

# ======================================================================
# HEALTH MANAGEMENT
# ======================================================================

def heal_character(character, amount):
    before = character["health"]
    character["health"] = min(character["max_health"], character["health"] + amount)
    return character["health"] - before

def is_character_dead(character):
    return character["health"] <= 0

def revive_character(character):
    if character["health"] > 0:
        return False  # Already alive
    character["health"] = max(1, character["max_health"] // 2)
    return True

# ======================================================================
# SAVE / LOAD CHARACTER
# ======================================================================

def save_character(character, save_directory="data/save_games"):
    os.makedirs(save_directory, exist_ok=True)
    path = os.path.join(save_directory, f"{character['name']}_save.txt")
    try:
        with open(path, "w") as f:
            for key, value in character.items():
                if isinstance(value, list):
                    value = ",".join(value)
                f.write(f"{key.upper()}: {value}\n")
        return True
    except Exception:
        raise  # Allow IOError / PermissionError to propagate

def load_character(character_name, save_directory="data/save_games"):
    path = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(path):
        raise CharacterNotFoundError(f"No save found for {character_name}")

    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Unable to read save file")

    character = {}
    for line in lines:
        if ":" not in line:
            raise InvalidSaveDataError("Malformed line in save")
        key, value = line.strip().split(":", 1)
        key = key.lower()
        value = value.strip()
        if key in ["inventory", "active_quests", "completed_quests"]:
            character[key] = value.split(",") if value else []
        else:
            character[key] = value

    for nf in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        try:
            character[nf] = int(character[nf])
        except Exception:
            raise InvalidSaveDataError(f"Invalid numeric data: {nf}")

    validate_character_data(character)
    return character

# ======================================================================
# LIST / DELETE CHARACTERS
# ======================================================================

def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    chars = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            chars.append(filename[:-9])
    return chars

def delete_character(character_name, save_directory="data/save_games"):
    path = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(path):
        raise CharacterNotFoundError(f"No save file for {character_name}")

    os.remove(path)
    return True

# ======================================================================
# VALIDATION
# ======================================================================

def validate_character_data(character):
    required_keys = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]
    for key in required_keys:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

    for nf in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        if not isinstance(character[nf], int):
            raise InvalidSaveDataError(f"Field {nf} must be an integer")

    for lf in ["inventory", "active_quests", "completed_quests"]:
        if not isinstance(character[lf], list):
            raise InvalidSaveDataError(f"Field {lf} must be a list")
    return True
