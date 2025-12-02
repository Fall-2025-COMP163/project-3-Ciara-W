"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Filled Implementation

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")
    
    quest = quest_data_dict[quest_id]
    if character['level'] < quest['required_level']:
        raise InsufficientLevelError("Level too low")
    if quest['prerequisite'] != "NONE" and quest['prerequisite'] not in character['completed_quests']:
        raise QuestRequirementsNotMetError("Prerequisite quest not completed")
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError("Quest already completed")
    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError("Quest already active")
    
    character['active_quests'].append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError("Quest not active")
    
    quest = quest_data_dict[quest_id]
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    # Grant rewards
    character['experience'] = character.get('experience', 0) + quest['reward_xp']
    character['gold'] = character.get('gold', 0) + quest['reward_gold']
    return {'xp': quest['reward_xp'], 'gold': quest['reward_gold']}

def abandon_quest(character, quest_id):
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError("Quest not active")
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    return [quest_data_dict[q] for q in character['active_quests'] if q in quest_data_dict]

def get_completed_quests(character, quest_data_dict):
    return [quest_data_dict[q] for q in character['completed_quests'] if q in quest_data_dict]

def get_available_quests(character, quest_data_dict):
    available = []
    for qid, quest in quest_data_dict.items():
        if qid in character['completed_quests'] or qid in character['active_quests']:
            continue
        if character['level'] >= quest['required_level']:
            prereq = quest['prerequisite']
            if prereq == "NONE" or prereq in character['completed_quests']:
                available.append(quest)
    return available

def is_quest_completed(character, quest_id):
    return quest_id in character['completed_quests']

def is_quest_active(character, quest_id):
    return quest_id in character['active_quests']

def can_accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]
    if quest_id in character['completed_quests'] or quest_id in character['active_quests']:
        return False
    if character['level'] < quest['required_level']:
        return False
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        return False
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")
    chain = []
    current = quest_id
    while current != "NONE":
        chain.insert(0, current)
        current = quest_data_dict[current]['prerequisite']
    return chain

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    completed = len(character['completed_quests'])
    if total == 0:
        return 0.0
    return (completed / total) * 100

def get_total_quest_rewards_earned(character, quest_data_dict):
    xp = sum(quest_data_dict[q]['reward_xp'] for q in character['completed_quests'] if q in quest_data_dict)
    gold = sum(quest_data_dict[q]['reward_gold'] for q in character['completed_quests'] if q in quest_data_dict)
    return {'total_xp': xp, 'total_gold': gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [q for q in quest_data_dict.values() if min_level <= q['required_level'] <= max_level]

def display_quest_info(quest_data):
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Reward XP: {quest_data['reward_xp']}, Gold: {quest_data['reward_gold']}")
    print(f"Required Level: {quest_data['required_level']}, Prerequisite: {quest_data['prerequisite']}")

def display_quest_list(quest_list):
    for q in quest_list:
        print(f"- {q['title']} (Level {q['required_level']}) - XP: {q['reward_xp']}, Gold: {q['reward_gold']}")

def display_character_quest_progress(character, quest_data_dict):
    active = len(character['active_quests'])
    completed = len(character['completed_quests'])
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    print(f"\nQuest Progress: {completed} completed, {active} active, {percent:.1f}% complete")
    print(f"Total rewards earned: XP {rewards['total_xp']}, Gold {rewards['total_gold']}")

def validate_quest_prerequisites(quest_data_dict):
    for qid, quest in quest_data_dict.items():
        prereq = quest['prerequisite']
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Invalid prerequisite: {prereq}")
    return True

# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }

    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
        rewards = complete_quest(test_char, 'first_quest', test_quests)
        print(f"Quest completed! Rewards: {rewards}")
    except Exception as e:
        print(f"Error: {e}")
