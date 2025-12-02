"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Completed Beginner Version

Name: [Your Name Here]

AI Usage: Code assistance used for completing missing TODO sections with
beginner-level logic. No advanced algorithms were used.
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

import random

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """Create an enemy based on type."""
    enemy_type = enemy_type.lower()

    if enemy_type == "goblin":
        return {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        }

    elif enemy_type == "orc":
        return {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        }

    elif enemy_type == "dragon":
        return {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }

    else:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' not recognized.")


def get_random_enemy_for_level(character_level):
    """Returns a level-appropriate enemy."""
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:

    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        """Run the combat loop until someone dies."""
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is already dead!")

        display_battle_log("Battle begins!")

        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            # Player turn
            self.player_turn()
            result = self.check_battle_end()
            if result:
                self.combat_active = False
                break

            # Enemy turn
            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                self.combat_active = False
                break

        # Return results
        if result == "player":
            rewards = get_victory_rewards(self.enemy)
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"]
            }
        else:
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        print("\n--- Player Turn ---")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run Away")

        choice = input("Choose action (1-3): ")

        if choice == "1":
            dmg = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, dmg)
            display_battle_log(f"You deal {dmg} damage!")

        elif choice == "2":
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)

        elif choice == "3":
            success = self.attempt_escape()
            if success:
                display_battle_log("You escaped successfully!")
                self.combat_active = False
            else:
                display_battle_log("Escape failed!")

        else:
            display_battle_log("Invalid choice — you lose your turn!")

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        print("\n--- Enemy Turn ---")
        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"{self.enemy['name']} hits you for {dmg} damage!")

    def calculate_damage(self, attacker, defender):
        raw_damage = attacker["strength"] - (defender["strength"] // 4)
        if raw_damage < 1:
            raw_damage = 1
        return raw_damage

    def apply_damage(self, target, damage):
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0

    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            return "player"
        if self.character["health"] <= 0:
            return "enemy"
        return None

    def attempt_escape(self):
        chance = random.randint(1, 2)
        return chance == 1


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """Executes character's special ability based on class."""
    char_class = character["class"].lower()

    if char_class == "warrior":
        return warrior_power_strike(character, enemy)

    elif char_class == "mage":
        return mage_fireball(character, enemy)

    elif char_class == "rogue":
        return rogue_critical_strike(character, enemy)

    elif char_class == "cleric":
        return cleric_heal(character)

    else:
        return "No special ability for this class."


def warrior_power_strike(character, enemy):
    dmg = character["strength"] * 2
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Power Strike! You deal {dmg} damage."


def mage_fireball(character, enemy):
    dmg = character["magic"] * 2
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Fireball hits for {dmg} damage!"


def rogue_critical_strike(character, enemy):
    if random.randint(1, 2) == 1:
        dmg = character["strength"] * 3
        msg = "Critical hit! Massive damage!"
    else:
        dmg = character["strength"]
        msg = "Normal hit."
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"{msg} You deal {dmg} damage."


def cleric_heal(character):
    healed = 30
    character["health"] += healed
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]
    return f"You heal yourself for {healed} HP."


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def can_character_fight(character):
    return character["health"] > 0


def get_victory_rewards(enemy):
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }


def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")


def display_battle_log(message):
    print(f">>> {message}")


# ============================================================================
# MAIN TEST (Optional)
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")

    hero = {
        "name": "Hero",
        "class": "Warrior",
        "health": 120,
        "max_health": 120,
        "strength": 15,
        "magic": 5
    }

    enemy = create_enemy("goblin")

    battle = SimpleBattle(hero, enemy)
    results = battle.start_battle()
    print("\nBattle Results:", results)

