"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """Loads quests from a text file into a dictionary."""
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    try:
        with open(filename, "r") as f:
            content = f.read().strip()

        if not content:
            raise InvalidDataFormatError("Quest file is empty or invalid")

        quests = {}
        blocks = content.split("\n\n")

        for block in blocks:
            lines = block.strip().split("\n")
            quest = parse_quest_block(lines)
            validate_quest_data(quest)
            quests[quest["quest_id"]] = quest

        return quests

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading quest file: {e}")


def load_items(filename="data/items.txt"):
    """Loads items from a text file into a dictionary."""
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    try:
        with open(filename, "r") as f:
            content = f.read().strip()

        if not content:
            raise InvalidDataFormatError("Item file is empty or invalid")

        items = {}
        blocks = content.split("\n\n")

        for block in blocks:
            lines = block.strip().split("\n")
            item = parse_item_block(lines)
            validate_item_data(item)
            items[item["item_id"]] = item

        return items

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading item file: {e}")


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    """Ensures a quest has all required fields."""
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {key}")

    # Ensure numeric fields are ints
    try:
        quest_dict["reward_xp"] = int(quest_dict["reward_xp"])
        quest_dict["reward_gold"] = int(quest_dict["reward_gold"])
        quest_dict["required_level"] = int(quest_dict["required_level"])
    except ValueError:
        raise InvalidDataFormatError("Quest numeric fields must be integers")

    return True


def validate_item_data(item_dict):
    """Ensures an item has valid fields and types."""
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {key}")

    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    try:
        item_dict["cost"] = int(item_dict["cost"])
    except ValueError:
        raise InvalidDataFormatError("Item cost must be an integer")

    return True


# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """Parses text lines into a quest dict."""
    quest = {}

    try:
        for line in lines:
            if ": " not in line:
                continue
            key, val = line.split(": ", 1)
            key = key.lower()

            if key == "quest_id":
                quest["quest_id"] = val
            elif key == "title":
                quest["title"] = val
            elif key == "description":
                quest["description"] = val
            elif key == "reward_xp":
                quest["reward_xp"] = int(val)
            elif key == "reward_gold":
                quest["reward_gold"] = int(val)
            elif key == "required_level":
                quest["required_level"] = int(val)
            elif key == "prerequisite":
                quest["prerequisite"] = val

        return quest

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")


def parse_item_block(lines):
    """Parses text lines into an item dict."""
    item = {}

    try:
        for line in lines:
            if ": " not in line:
                continue
            key, val = line.split(": ", 1)
            key = key.lower()

            if key == "item_id":
                item["item_id"] = val
            elif key == "name":
                item["name"] = val
            elif key == "type":
                item["type"] = val
            elif key == "effect":
                item["effect"] = val
            elif key == "cost":
                item["cost"] = int(val)
            elif key == "description":
                item["description"] = val

        return item

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")


# ============================================================================
# CREATE MISSING DATA FILES
# ============================================================================

def create_default_data_files():
    """Creates data/ and starter files if missing."""
    os.makedirs("data", exist_ok=True)

    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w") as f:
            f.write(
                "QUEST_ID: first_quest\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Complete your first quest\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 25\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w") as f:
            f.write(
                "ITEM_ID: health_potion\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 10\n"
                "DESCRIPTION: Restores health\n"
            )
