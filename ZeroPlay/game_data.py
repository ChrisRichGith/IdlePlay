# game_data.py
"""
Contains static game data, such as class definitions.
"""

CLASSES = {
    "Krieger": {
        "description": "Ein Meister des Nahkampfs, robust und stark.",
        "attributes": {'Stärke': 8, 'Agilität': 4, 'Intelligenz': 3, 'Glück': 4},
        "main_stat": "Stärke",
        "allowed_armor": ["Kette", "Platte"],
        "image_path": "assets/krieger.png"
    },
    "Magier": {
        "description": "Ein weiser Gelehrter, der arkane Energien bändigt.",
        "attributes": {'Stärke': 3, 'Agilität': 5, 'Intelligenz': 8, 'Glück': 4},
        "main_stat": "Intelligenz",
        "allowed_armor": ["Stoff"],
        "image_path": "assets/magier.png"
    },
    "Schurke": {
        "description": "Ein listiger Halunke, der schnell und präzise zuschlägt.",
        "attributes": {'Stärke': 4, 'Agilität': 8, 'Intelligenz': 3, 'Glück': 6},
        "main_stat": "Agilität",
        "allowed_armor": ["Leder"],
        "image_path": "assets/schurke.png"
    }
}

ITEM_BLUEPRINTS = {
    # Nomen: (Name, Artikel)
    "Waffe": [
        {"name": ("Schwert", "n"), "base_stat": "Stärke", "base_bonus": 2},
        {"name": ("Stab", "m"), "base_stat": "Intelligenz", "base_bonus": 2},
        {"name": ("Dolch", "m"), "base_stat": "Agilität", "base_bonus": 2},
    ],
    "Kopf": [
        {"name": ("Kettenhaube", "f"), "base_stat": "Stärke", "base_bonus": 1, "armor_type": "Kette"},
        {"name": ("Stoffhut", "m"), "base_stat": "Intelligenz", "base_bonus": 1, "armor_type": "Stoff"},
        {"name": ("Lederkapuze", "f"), "base_stat": "Agilität", "base_bonus": 1, "armor_type": "Leder"},
    ],
    "Brust": [
        {"name": ("Plattenpanzer", "m"), "base_stat": "Stärke", "base_bonus": 3, "armor_type": "Platte"},
        {"name": ("Stoffrobe", "f"), "base_stat": "Intelligenz", "base_bonus": 3, "armor_type": "Stoff"},
        {"name": ("Lederwams", "n"), "base_stat": "Agilität", "base_bonus": 2, "armor_type": "Leder"},
    ]
}

RARITIES = {
    "Schlecht":     {"color": "#B0B0B0", "modifier": 0.7, "min_level": 1, "weight": 10, "max_upgrades": 2},
    "Gewöhnlich":   {"color": "#FFFFFF", "modifier": 1.0, "min_level": 1, "weight": 70, "max_upgrades": 3},
    "Ungewöhnlich": {"color": "#1EFF00", "modifier": 1.2, "min_level": 5, "weight": 15, "max_upgrades": 5},
    "Selten":       {"color": "#68AFFF", "modifier": 1.5, "min_level": 15, "weight": 4,  "max_upgrades": 7},
    "Episch":       {"color": "#A335EE", "modifier": 1.8, "min_level": 30, "weight": 1,  "max_upgrades": 10},
    "Legendär":     {"color": "#FF8000", "modifier": 2.2, "min_level": 50, "weight": 0.1,"max_upgrades": 13},
    "Mythisch":     {"color": "#E5CC80", "modifier": 2.7, "min_level": 75, "weight": 0.01,"max_upgrades": 15}
}

ITEM_ICONS = {
    "Waffe": "🗡️",
    "Schild": "🛡️",
    "Kopf": "👑",
    "Brust": "👕",
    "Beine": "👖",
    "Füße": "👢",
    "Verbrauchsgut": "🧪"
}

POTIONS = [
    # LP Potions
    {"level_req": 1, "name": "Kleiner Heiltrank", "type": "LP", "value": 50, "cost": 25},
    {"level_req": 10, "name": "Heiltrank", "type": "LP", "value": 150, "cost": 100},
    {"level_req": 25, "name": "Großer Heiltrank", "type": "LP", "value": 500, "cost": 500},
    {"level_req": 50, "name": "Überragender Heiltrank", "type": "LP", "value": 2000, "cost": 2500},

    # Mana Potions
    {"level_req": 1, "name": "Kleiner Manatrank", "type": "MP", "value": 30, "cost": 35},
    {"level_req": 10, "name": "Manatrank", "type": "MP", "value": 100, "cost": 120},
    {"level_req": 25, "name": "Großer Manatrank", "type": "MP", "value": 400, "cost": 600},
    {"level_req": 50, "name": "Überragender Manatrank", "type": "MP", "value": 1500, "cost": 3000},

    # Energie Potions
    {"level_req": 1, "name": "Kleiner Energietrank", "type": "Energie", "value": 30, "cost": 35},
    {"level_req": 10, "name": "Energietrank", "type": "Energie", "value": 100, "cost": 120},

    # Wut Potions
    {"level_req": 1, "name": "Kleiner Wuttrank", "type": "Wut", "value": 20, "cost": 40},
    {"level_req": 10, "name": "Wuttrank", "type": "Wut", "value": 75, "cost": 130},
]

WARRIOR_EVENTS = [
    "Du schmetterst deinen Schild in einen Gegner.",
    "Mit einem mächtigen Hieb spaltest du einen Helm.",
    "Du parierst einen Angriff und konterst.",
    "Ein lauter Schlachtruf lässt deine Feinde erzittern.",
    "Du trittst eine Kiste auf und findest eine Münze.",
    "Dein Schwert trifft zielsicher.",
]

MAGE_EVENTS = [
    "Ein Feuerball schlägt zischend in die Gegnerreihen ein.",
    "Du wirkst einen Schutzzauber, der einen Hieb abwehrt.",
    "Eissplitter frieren einen Angreifer an Ort und Stelle fest.",
    "Ein Kettenblitz springt von einem Feind zum nächsten.",
    "Du murmelst eine arkane Formel und stärkst deine Waffe.",
    "Du findest eine alte Schriftrolle.",
]

ROGUE_EVENTS = [
    "Du springst aus den Schatten und landest einen kritischen Treffer.",
    "Mit einem schnellen Schnitt entwaffnest du einen Gegner.",
    "Du wirfst einen Dolch präzise auf ein entferntes Ziel.",
    "Eine Rauchbombe sorgt für Verwirrung.",
    "Du knackst eine kleine Schatulle und findest Gold.",
    "Du weichst einer Falle geschickt aus.",
]

BOSS_TIERS = [
    {
        "tier": 0,
        "name": "Goblin König",
        "hp": 150,
        "damage": (10, 20),
        "image_path": "assets/bosses/goblin_king.png",
        "required_item_level": 0  # First boss is always available
    },
    {
        "tier": 1,
        "name": "Steingolem",
        "hp": 250,
        "damage": (15, 25),
        "image_path": "assets/bosses/stone_golem.png",
        "required_item_level": 20
    },
    {
        "tier": 2,
        "name": "Chimären-Matriarchin",
        "hp": 400,
        "damage": (25, 40),
        "image_path": "assets/bosses/chimaeren_matriarchin.png",
        "required_item_level": 45
    },
    {
        "tier": 3,
        "name": "Nekromanten-Lord",
        "hp": 650,
        "damage": (40, 60),
        "image_path": "assets/bosses/nekromanten_lord.png",
        "required_item_level": 75
    },
    {
        "tier": 4,
        "name": "Eisriesen-Häuptling",
        "hp": 1000,
        "damage": (60, 80),
        "image_path": "assets/bosses/eisriesen_haeuptling.png",
        "required_item_level": 110
    },
    {
        "tier": 5,
        "name": "Alter Drache",
        "hp": 1500,
        "damage": (80, 120),
        "image_path": "assets/bosses/alter_drache.png",
        "required_item_level": 150
    }
]


# --- Components for procedural text generation ---

QUEST_LOCATIONS = [
    "in den düsteren Wäldern",
    "zu den vergessenen Ruinen",
    "durch die sengende Wüste",
    "über die eisigen Gipfel",
    "tief in die Goblin-Minen",
]

QUEST_ACTIONS_PREFIX = [
    "Dort angekommen, musst du",
    "Deine Aufgabe ist es,",
    "Im Zielgebiet angekommen, gilt es,",
]

QUEST_RETURNS = [
    "Nach getaner Arbeit machst du dich auf den Rückweg.",
    "Die Aufgabe ist erfüllt und du trittst die Heimreise an.",
    "Erschöpft, aber erfolgreich, beginnst du den Rückmarsch.",
]

