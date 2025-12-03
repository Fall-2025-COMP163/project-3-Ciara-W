"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Filled Implementation

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================

def add_item_to_inventory(character, item_id):
    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Cannot add {item_id}: Inventory full")
    character.setdefault('inventory', []).append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"{item_id} not found in inventory")
    inventory.remove(item_id)
    return True


def has_item(character, item_id):
    return item_id in character.get('inventory', [])


def count_item(character, item_id):
    return character.get('inventory', []).count(item_id)


def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character.get('inventory', []))


def clear_inventory(character):
    removed_items = character.get('inventory', []).copy()
    character['inventory'] = []
    return removed_items

# ============================================================================

def parse_item_effect(effect_string):
    stat, value = effect_string.split(":")
    return stat.strip(), int(value)


def apply_stat_effect(character, stat_name, value):
    # Ensure stat exists
    if stat_name not in character:
        character[stat_name] = 0

    # Increase stat
    character[stat_name] += value

    # Clamp health to max
    if stat_name == "health":
        max_hp = character.get("max_health", 100)
        character["health"] = min(character["health"], max_hp)

# ============================================================================

def use_item(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"{item_id} not in inventory")

    if item_data['type'] != 'consumable':
        raise InvalidItemTypeError(f"{item_id} cannot be used")

    # Apply effect
    stat, val = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat, val)

    # Remove item
    remove_item_from_inventory(character, item_id)

    return f"{item_id} used! {stat} increased by {val}."


def equip_weapon(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"{item_id} not in inventory")

    if item_data['type'] != 'weapon':
        raise InvalidItemTypeError(f"{item_id} is not a weapon")

    # Unequip any weapon
    if character.get('equipped_weapon'):
        unequip_weapon(character)

    stat, val = parse_item_effect(item_data['effect'])
    character[stat] = character.get(stat, 0) + val

    character['equipped_weapon'] = item_id
    remove_item_from_inventory(character, item_id)

    return f"{item_id} equipped! {stat} +{val}"


def equip_armor(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"{item_id} not in inventory")

    if item_data['type'] != 'armor':
        raise InvalidItemTypeError(f"{item_id} is not armor")

    if character.get('equipped_armor'):
        unequip_armor(character)

    stat, val = parse_item_effect(item_data['effect'])
    character[stat] = character.get(stat, 0) + val

    character['equipped_armor'] = item_id
    remove_item_from_inventory(character, item_id)

    return f"{item_id} equipped! {stat} +{val}"


def unequip_weapon(character):
    weapon = character.get('equipped_weapon')
    if not weapon:
        return None

    character['equipped_weapon'] = None
    add_item_to_inventory(character, weapon)

    return weapon


def unequip_armor(character):
    armor = character.get('equipped_armor')
    if not armor:
        return None

    character['equipped_armor'] = None
    add_item_to_inventory(character, armor)

    return armor

# ============================================================================

def purchase_item(character, item_id, item_data):
    cost = item_data.get('cost', 0)

    # Check gold
    if character.get('gold', 0) < cost:
        raise InsufficientResourcesError(f"Not enough gold for {item_id}")

    # Check space
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError(f"Inventory full, cannot buy {item_id}")

    # Spend gold
    character['gold'] -= cost

    # Add item
    add_item_to_inventory(character, item_id)

    return True


def sell_item(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"{item_id} not in inventory")

    price = item_data.get('cost', 0) // 2

    remove_item_from_inventory(character, item_id)
    character['gold'] = character.get('gold', 0) + price

    return price

# ============================================================================

def display_inventory(character, item_data_dict):
    inventory = character.get('inventory', [])

    counted = {}
    for item in inventory:
        counted[item] = counted.get(item, 0) + 1

    print("=== Inventory ===")
    for item_id, qty in counted.items():
        name = item_data_dict.get(item_id, {}).get('name', item_id)
        type_ = item_data_dict.get(item_id, {}).get('type', 'Unknown')
        print(f"{name} ({type_}) x{qty}")

    print(f"Gold: {character.get('gold', 0)}")
    print("=================")
