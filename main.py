"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module

Name: [Your Name Here]
AI Usage: [Document any AI assistance used]
"""

import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================ #
# GAME STATE
# ============================================================================ #

current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================ #
# MAIN MENU
# ============================================================================ #

def main_menu():
    print("\nMAIN MENU")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    choice = input("Choose an option: ")
    return int(choice) if choice.isdigit() else 0

def new_game():
    global current_character
    while True:
        name = input("Enter your character's name: ")
        char_class = input("Choose a class (Warrior, Mage, Rogue, Cleric): ")
        try:
            current_character = character_manager.create_character(name, char_class)
            print(f"Character {name} the {char_class} created!")
            save_game()
            game_loop()
            break
        except InvalidCharacterClassError:
            print("Invalid class. Try again.")

def load_game():
    global current_character
    try:
        saved = character_manager.list_saved_characters()
        if not saved:
            print("No saved characters found.")
            return
        print("Saved characters:")
        for i, name in enumerate(saved, start=1):
            print(f"{i}. {name}")
        choice = int(input("Choose a character to load: ")) - 1
        current_character = character_manager.load_character(saved[choice])
        print(f"Loaded character: {current_character['name']}")
        game_loop()
    except (CharacterNotFoundError, SaveFileCorruptedError):
        print("Failed to load character.")

# ============================================================================ #
# GAME LOOP
# ============================================================================ #

def game_loop():
    global game_running
    game_running = True
    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting...")
            game_running = False
        else:
            print("Invalid choice. Select 1-6.")

def game_menu():
    print("\nGAME MENU")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")
    choice = input("Choose an option: ")
    return int(choice) if choice.isdigit() else 0

# ============================================================================ #
# GAME ACTIONS
# ============================================================================ #

def view_character_stats():
    print("\nCHARACTER STATS")
    for k, v in current_character.items():
        if k != 'inventory':
            print(f"{k.capitalize()}: {v}")
    print("Active Quests:", current_character.get('active_quests', []))
    print("Completed Quests:", current_character.get('completed_quests', []))

def view_inventory():
    try:
        print("\nINVENTORY:")
        for i, item in enumerate(current_character.get('inventory', []), start=1):
            print(f"{i}. {item}")
        print("Options: Use, Equip, Drop, Back")
        # Placeholder for inventory actions
    except InventoryFullError as e:
        print(e)

def quest_menu():
    print("\nQUEST MENU")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest")
    print("7. Back")
    choice = input("Choose an option: ")
    # Implement quest handling using quest_handler here
    # Placeholder

def explore():
    print("\nExploring...")
    enemy = combat_system.create_enemy("goblin")
    battle = combat_system.SimpleBattle(current_character, enemy)
    battle.start_battle()
    if current_character['health'] <= 0:
        handle_character_death()

def shop():
    try:
        print("\nSHOP")
        print("Available items:")
        for name, data in all_items.items():
            print(f"{name}: {data.get('cost', 0)} gold")
        # Placeholder for purchase/sell actions
    except InsufficientResourcesError as e:
        print(e)

# ============================================================================ #
# HELPER FUNCTIONS
# ============================================================================ #

def save_game():
    try:
        character_manager.save_character(current_character)
        print(f"{current_character['name']} saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    global all_quests, all_items
    all_quests = game_data.load_quests("data/quests.txt") or {}
    all_items = game_data.load_items("data/items.txt") or {}

def handle_character_death():
    global game_running
    print("\nYour character has died!")
    choice = input("Revive for 50 gold? (yes/no): ").lower()
    if choice == 'yes' and current_character.get('gold', 0) >= 50:
        character_manager.revive_character(current_character)
        current_character['gold'] -= 50
        print("Character revived!")
    else:
        print("Game over.")
        game_running = False

def display_welcome():
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("Welcome to Quest Chronicles!\nBuild your character, complete quests, and become a legend!")

# ============================================================================ #
# MAIN EXECUTION
# ============================================================================ #

def main():
    display_welcome()
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except (MissingDataFileError, InvalidDataFormatError):
        print("Game data missing or corrupted. Creating default data...")
        game_data.create_default_data_files()
        load_game_data()

    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Thanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Select 1-3.")

if __name__ == "__main__":
    main()

