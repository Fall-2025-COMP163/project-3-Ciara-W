"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]
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
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")
    
    quests = {}
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                raise InvalidDataFormatError("Quest file is empty or invalid")
            
            blocks = content.split("\n\n")
            for block in blocks:
                lines = block.strip().split("\n")
                quest = parse_quest_block(lines)
                validate_quest_data(quest)
                quests[quest['quest_id']] = quest
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading quest file: {e}")
    
    return quests

def load_items(filename="data/items.txt"):
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")
    
    items = {}
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                raise InvalidDataFormatError("Item file is empty or invalid")
            
            blocks = content.split("\n\n")
            for block in blocks:
                lines = block.strip().split("\n")
                item = parse_item_block(lines)
                validate_item_data(item)
                items[item['item_id']] = item
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading item file: {e}")
    
    return items

# ============================================================================ 
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    required_fields = [
        'quest_id', 'title', 'description', 
        'reward_xp', 'reward_gold', 'required_level', 'prerequisite'
    ]
    for key in required_fields:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {key}")
    
    # Ensure numeric fields are integers
    for field in ['reward_xp', 'reward_gold', 'required_level']:
        try:
            quest_dict[field] = int(quest_dict[field])
        except ValueError:
            raise InvalidDataFormatError(f"Quest field {field} must be an integer")
    
    return True

def validate_item_data(item_dict):
    required_fields = ['item_id', 'name', 'type', 'effect', 'cost', 'description']
    for key in required_fields:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {key}")
    
    if item_dict['type'] not in ['weapon', 'armor', 'consumable']:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    
    try:
        item_dict['cost'] = int(item_dict['cost'])
    except ValueError:
        raise InvalidDataFormatError("Item cost must be an integer")
    
    return True

# ============================================================================ 
# PARSING FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    quest = {}
    try:
        for line in lines:
            if ": " not in line:
                continue
            key, value = line.split(": ", 1)
            key = key.lower()
            if key == 'quest_id':
                quest['quest_id'] = value
            elif key == 'title':
                quest['title'] = value
            elif key == 'description':
                quest['description'] = value
            elif key == 'reward_xp':
                quest['reward_xp'] = int(value)
            elif key == 'reward_gold':
                quest['reward_gold'] = int(value)
            elif key == 'required_level':
                quest['required_level'] = int(value)
            elif key == 'prerequisite':
                quest['prerequisite'] = value
        return quest
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")

def parse_item_block(lines):
    item = {}
    try:
        for line in lines:
            if ": " not in line:
                continue
            key, value = line.split(": ", 1)
            key = key.lower()
            if key == 'item_id':
                item['item_id'] = value
            elif key == 'name':
                item['name'] = value
            elif key == 'type':
                item['type'] = value
            elif key == 'effect':
                item['effect'] = value
            elif key == 'cost':
                item['cost'] = int(value)
            elif key == 'description':
                item['description'] = value
        return item
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")

# ============================================================================ 
# DEFAULT FILE CREATION
# ============================================================================

def create_default_data_files():
    os.makedirs("data", exist_ok=True)
    
    quest_file = "data/quests.txt"
    item_file = "data/items.txt"
    
    if not os.path.exists(quest_file):
        with open(quest_file, "w") as f:
            f.write(
                "QUEST_ID: first_quest\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Complete your first quest\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 25\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )
    
    if not os.path.exists(item_file):
        with open(item_file, "w") as f:
            f.write(
                "ITEM_ID: health_potion\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 10\n"
                "DESCRIPTION: Restores 20 health points\n"
            )

