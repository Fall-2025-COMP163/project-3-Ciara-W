"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module
"""

import character_manager
from custom_exceptions import *

# ============================================================================ #
# GAME STATE
# ============================================================================ #

current_character = None
game_running = False

# ============================================================================ #
# MAIN MENU FUNCTIONS
# ============================================================================ #

def main_menu():
    return 3  # Minimal placeholder: will choose Exit automatically

def new_game():
    global current_character
    # Minimal placeholder: just create a default character
    current_character = character_manager.create_character("TestHero", "Warrior")

def load_game():
    global current_character
    # Minimal placeholder: do nothing
    pass

def game_loop():
    global game_running
    game_running = True
    while game_running:
        # Immediately exit loop
        game_running = False

def save_game():
    if current_character:
        character_manager.save_character(current_character)

def load_game_data():
    # Minimal placeholder: do nothing
    pass

# ============================================================================ #
# MAIN EXECUTION
# ============================================================================ #

def main():
    load_game_data()
    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            break

if __name__ == "__main__":
    main()


