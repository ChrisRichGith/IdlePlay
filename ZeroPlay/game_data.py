# game_data.py
"""
Contains static game data, such as class definitions.
"""
from boss import Boss
from item import Item, generate_random_item

# Note: The actual translation is handled by get_text() in the UI.
# These dictionaries now store keys or data needed for dynamic text generation.

CLASSES = {
    "Krieger": {
        "description_key": "warrior_desc",
        "attributes": {'Stärke': 8, 'Agilität': 4, 'Intelligenz': 3, 'Glück': 4},
        "main_stat": "Stärke",
        "allowed_armor": ["Kette", "Platte"],
        "image_path": "assets/krieger.png"
    },
    "Magier": {
        "description_key": "mage_desc",
        "attributes": {'Stärke': 3, 'Agilität': 5, 'Intelligenz': 8, 'Glück': 4},
        "main_stat": "Intelligenz",
        "allowed_armor": ["Stoff"],
        "image_path": "assets/magier.png"
    },
    "Schurke": {
        "description_key": "rogue_desc",
        "attributes": {'Stärke': 4, 'Agilität': 8, 'Intelligenz': 3, 'Glück': 6},
        "main_stat": "Agilität",
        "allowed_armor": ["Leder"],
        "image_path": "assets/schurke.png"
    }
}

ITEM_BLUEPRINTS = {
    "Waffe": [
        {"name_key": "item_sword", "base_stat": "Stärke", "base_bonus": 2},
        {"name_key": "item_staff", "base_stat": "Intelligenz", "base_bonus": 2},
        {"name_key": "item_dagger", "base_stat": "Agilität", "base_bonus": 2},
    ],
    # ... other item blueprints would follow the same pattern
}

RARITIES = {
    "rarity_schlecht":     {"color": "#B0B0B0", "modifier": 0.7, "min_level": 1, "weight": 10},
    "rarity_gewöhnlich":   {"color": "#FFFFFF", "modifier": 1.0, "min_level": 1, "weight": 70},
    "rarity_ungewöhnlich": {"color": "#1EFF00", "modifier": 1.2, "min_level": 5, "weight": 15},
    "rarity_selten":       {"color": "#68AFFF", "modifier": 1.5, "min_level": 15, "weight": 4},
    "rarity_episch":       {"color": "#A335EE", "modifier": 1.8, "min_level": 30, "weight": 1},
    "rarity_legendär":     {"color": "#FF8000", "modifier": 2.2, "min_level": 50, "weight": 0.1},
    "rarity_mythisch":     {"color": "#E5CC80", "modifier": 2.7, "min_level": 75, "weight": 0.01}
}

POTIONS = [
    {"level_req": 1, "name_key": "potion_small_healing", "type": "LP", "value": 50, "cost": 25},
    {"level_req": 10, "name_key": "potion_healing", "type": "LP", "value": 150, "cost": 100},
    # ... other potions
]

# ... (Event texts are not translated as they are developer-facing logs)

QUEST_LOCATIONS = [
    "quest_location_forest",
    "quest_location_ruins",
    "quest_location_desert",
    "quest_location_peaks",
    "quest_location_mines",
]
QUEST_ACTIONS_PREFIX = [
    "quest_action_prefix_1",
    "quest_action_prefix_2",
    "quest_action_prefix_3",
]
QUEST_RETURNS = [
    "quest_return_1",
    "quest_return_2",
    "quest_return_3",
]

AVAILABLE_BOSSES = [
    Boss(
        name="boss_raging_boar", # Now a key
        max_hp=100,
        attack=10,
        defense=5,
        reward={'xp': 50, 'copper': 100, 'items': []}
    ),
    Boss(
        name="boss_slime_king", # Now a key
        max_hp=250,
        attack=15,
        defense=10,
        reward={'xp': 150, 'copper': 300, 'items': [generate_random_item(10)]}
    ),
]
