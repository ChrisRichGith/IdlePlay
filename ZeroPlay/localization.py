# localization.py
"""
Handles localization and translation for the game.
"""

# The currently selected language code (e.g., 'de' for German, 'en' for English)
CURRENT_LANGUAGE = 'de'

# Dictionary containing all translatable strings in the game
TEXTS = {
    # Start Menu
    'main_menu_title': {'de': "Chronicle of the Idle Hero - Hauptmenü", 'en': "Chronicle of the Idle Hero - Main Menu"},
    'instructions_title': {'de': "Spielanleitung", 'en': "Instructions"},
    'intro_text': {
        'de': ("Willkommen bei Chronicle of the Idle Hero!\n\n"
               "Wähle einen Spielstand oder erstelle einen neuen Helden. "
               "Dein Held wird automatisch Quests erledigen. Deine Aufgabe ist es, "
               "seine Ausrüstung zu verwalten und Tränke zu kaufen.\n\n"
               "ACHTUNG: Wenn dein Held stirbt, wird sein Spielstand endgültig gelöscht!"),
        'en': ("Welcome to Chronicle of the Idle Hero!\n\n"
               "Select a save file or create a new hero. "
               "Your hero will complete quests automatically. Your task is to "
               "manage their equipment and buy potions.\n\n"
               "WARNING: If your hero dies, their save file will be permanently deleted!")
    },
    'available_saves_label': {'de': "Verfügbare Spielstände:", 'en': "Available Saves:"},
    'preview_title': {'de': "Vorschau", 'en': "Preview"},
    'load_button': {'de': "Laden", 'en': "Load"},
    'new_game_button': {'de': "Neues Spiel", 'en': "New Game"},
    'highscores_button': {'de': "Highscores", 'en': "Highscores"},
    'quit_button': {'de': "Beenden", 'en': "Quit"},
    'name_label': {'de': "Name:", 'en': "Name:"},
    'level_label': {'de': "Level:", 'en': "Level:"},
    'gold_label': {'de': "Gold:", 'en': "Gold:"},

    # Class Selection
    'create_character_title': {'de': "Charakter erstellen", 'en': "Create Character"},
    'hero_name_label': {'de': "Name des Helden:", 'en': "Hero's Name:"},
    'choose_your_class_label': {'de': "Wähle deine Klasse:", 'en': "Choose your class:"},
    'class_info_title': {'de': "Klasseninfo", 'en': "Class Info"},
    'start_attributes_label': {'de': "Start-Attribute:", 'en': "Starting Attributes:"},
    'select_a_class_label': {'de': "Wähle eine Klasse", 'en': "Select a Class"},
    'no_image_available': {'de': "Kein Bild verfügbar", 'en': "No image available"},
    'image_error': {'de': "Bildfehler:\n{e}", 'en': "Image Error:\n{e}"},
    'start_adventure_button': {'de': "Abenteuer beginnen", 'en': "Start Adventure"},
    'back_to_main_menu_button': {'de': "Zurück zum Hauptmenü", 'en': "Back to Main Menu"},
    'missing_name_title': {'de': "Fehlender Name", 'en': "Missing Name"},
    'missing_name_message': {'de': "Bitte gib einen Namen für deinen Helden ein.", 'en': "Please enter a name for your hero."},
    'warrior': {'de': "Krieger", 'en': "Warrior"},
    'mage': {'de': "Magier", 'en': "Mage"},
    'rogue': {'de': "Schurke", 'en': "Rogue"},

    # Tooltips
    'tooltip_type': {'de': "Typ", 'en': "Type"},
    'tooltip_value': {'de': "Wert", 'en': "Value"},

    # RPG GUI
    'equipment_tab': {'de': "Ausrüstung", 'en': "Equipment"},
    'inventory_tab': {'de': "Inventar", 'en': "Inventory"},
    'equipped_gear_title': {'de': "Angelegte Ausrüstung", 'en': "Equipped Gear"},
    'backpack_title': {'de': "Rucksack", 'en': "Backpack"},
    'image_not_found': {'de': "Bild nicht\ngefunden:\n{path}", 'en': "Image not\nfound:\n{path}"},
    'error_loading_image': {'de': "Fehler beim\nLaden des Bildes:\n{e}", 'en': "Error loading\nimage:\n{e}"},
    'image_error_short': {'de': "Bildfehler:\n{e}", 'en': "Image Error:\n{e}"},
    'error_title': {'de': "Fehler", 'en': "Error"},

    # Trader GUI
    'trader_title': {'de': "Händler", 'en': "Trader"},
    'your_coins_label': {'de': "Deine Münzen:", 'en': "Your Coins:"},
    'expand_inventory_button': {'de': "Inventar erweitern", 'en': "Expand Inventory"},
    'cost_label': {'de': "Kosten:", 'en': "Cost:"},
    'your_inventory_sell_title': {'de': "Dein Inventar (Verkaufen)", 'en': "Your Inventory (Sell)"},
    'trader_offer_buy_title': {'de': "Händler-Angebot (Kaufen)", 'en': "Trader's Offer (Buy)"},
    'sell_button': {'de': "Verkaufen", 'en': "Sell"},
    'sell_junk_button': {'de': "Schrott verkaufen", 'en': "Sell Junk"},
    'buy_button': {'de': "Kaufen", 'en': "Buy"},
    'sell_warning_title': {'de': "Verkaufen", 'en': "Sell"},
    'sell_warning_message': {'de': "Bitte wähle einen Gegenstand zum Verkaufen aus.", 'en': "Please select an item to sell."},
    'sell_all_info_title': {'de': "Alles verkauft", 'en': "All Sold"},
    'sell_all_info_message': {'de': "{count} Gegenstand/Gegenstände für insgesamt {amount} verkauft.", 'en': "Sold {count} item(s) for a total of {amount}."},
    'nothing_to_sell_title': {'de': "Nichts zu verkaufen", 'en': "Nothing to Sell"},
    'nothing_to_sell_message': {'de': "Du hast keine Gegenstände, die kein Upgrade sind.", 'en': "You have no items that are not upgrades."},
    'upgrade_success_title': {'de': "Upgrade erfolgreich!", 'en': "Upgrade Successful!"},
    'upgrade_success_message': {'de': "Inventar für {cost} erweitert!", 'en': "Inventory expanded for {cost}!"},
    'not_enough_coins_title': {'de': "Nicht genug Münzen", 'en': "Not Enough Coins"},
    'not_enough_coins_message': {'de': "Du kannst dir dieses Upgrade nicht leisten.", 'en': "You cannot afford this upgrade."},
    'buy_warning_title': {'de': "Kaufen", 'en': "Buy"},
    'buy_warning_message': {'de': "Bitte wähle einen Gegenstand zum Kaufen aus.", 'en': "Please select an item to buy."},
    'buy_fail_title': {'de': "Kauf fehlgeschlagen", 'en': "Purchase Failed"},

    # Blacksmith GUI
    'blacksmith_title': {'de': "Schmiede", 'en': "Blacksmith"},
    'equipment_title': {'de': "Ausrüstung", 'en': "Equipment"},
    'upgrade_title': {'de': "Verbesserung", 'en': "Upgrade"},
    'select_item_prompt': {'de': "Wähle einen Gegenstand", 'en': "Select an item"},
    'current_stats_label': {'de': "Aktuelle Werte:", 'en': "Current Stats:"},
    'next_level_label': {'de': "Nächste Stufe:", 'en': "Next Level:"},
    'cost_label_blacksmith': {'de': "Kosten:", 'en': "Cost:"},
    'upgrade_button': {'de': "Verbessern", 'en': "Upgrade"},
    'your_resources_label': {'de': "Deine Ressourcen:", 'en': "Your Resources:"},
    'max_level_reached': {'de': "Maximale Stufe erreicht", 'en': "Maximum level reached"},
    'not_enough_resources_title': {'de': "Nicht genügend Ressourcen", 'en': "Not Enough Resources"},
    'not_enough_resources_message': {'de': "Du hast nicht genug Ressourcen für dieses Upgrade.", 'en': "You do not have enough resources for this upgrade."},
    'upgrade_success_title_blacksmith': {'de': "Erfolg!", 'en': "Success!"},
    'upgrade_success_message_blacksmith': {'de': "{item_name} wurde erfolgreich verbessert!", 'en': "{item_name} was successfully upgraded!"},

    # Boss Arena GUI
    'boss_arena_title': {'de': "Boss Arena", 'en': "Boss Arena"},
    'choose_opponent_label': {'de': "Gegner wählen", 'en': "Choose Opponent"},
    'fight_title': {'de': "Kampf", 'en': "Fight"},
    'start_fight_button': {'de': "Kampf starten!", 'en': "Start Fight!"},
    'attack_button': {'de': "Angreifen", 'en': "Attack"},
    'use_potion_button': {'de': "Heiltrank benutzen", 'en': "Use Healing Potion"},
    'flee_button': {'de': "Fliehen", 'en': "Flee"},
    'fight_begins_log': {'de': "Der Kampf gegen {boss_name} beginnt!", 'en': "The fight against {boss_name} begins!"},
    'player_attack_log': {'de': "Du greifst {boss_name} an und verursachst {damage} Schaden.", 'en': "You attack {boss_name} and deal {damage} damage."},
    'boss_attack_log': {'de': "{boss_name} greift an und fügt dir {damage} Schaden zu.", 'en': "{boss_name} attacks and deals {damage} damage to you."},
    'no_potions_log': {'de': "Du hast keine Heiltränke im Inventar!", 'en': "You have no healing potions in your inventory!"},
    'fled_log': {'de': "Du bist geflohen!", 'en': "You have fled!"},
    'victory_log': {'de': "Du hast {boss_name} besiegt!", 'en': "You have defeated {boss_name}!"},
    'rewards_log_header': {'de': "--- Belohnungen ---", 'en': "--- Rewards ---"},
    'loot_xp_log': {'de': "+{xp} XP", 'en': "+{xp} XP"},
    'loot_copper_log': {'de': "+{copper} Kupfer", 'en': "+{copper} Copper"},
    'loot_item_log': {'de': "Gegenstand erhalten: {item_name}", 'en': "Item received: {item_name}"},
    'loot_inventory_full_log': {'de': "(Inventar voll für {item_name})", 'en': "(Inventory full for {item_name})"},
    'level_up_log_header': {'de': "--- Level Up! ---", 'en': "--- Level Up! ---"},
    'defeat_log': {'de': "Du wurdest besiegt...", 'en': "You have been defeated..."},

    # Game Data: Classes
    'warrior_desc': {'de': "Ein Meister des Nahkampfs, robust und stark.", 'en': "A master of close combat, sturdy and strong."},
    'mage_desc': {'de': "Ein weiser Gelehrter, der arkane Energien bändigt.", 'en': "A wise scholar who commands arcane energies."},
    'rogue_desc': {'de': "Ein listiger Halunke, der schnell und präzise zuschlägt.", 'en': "A cunning rogue who strikes with speed and precision."},

    # Game Data: Item Rarities
    'rarity_schlecht': {'de': "Schlecht", 'en': "Poor"},
    'rarity_gewöhnlich': {'de': "Gewöhnlich", 'en': "Common"},
    'rarity_ungewöhnlich': {'de': "Ungewöhnlich", 'en': "Uncommon"},
    'rarity_selten': {'de': "Selten", 'en': "Rare"},
    'rarity_episch': {'de': "Episch", 'en': "Epic"},
    'rarity_legendär': {'de': "Legendär", 'en': "Legendary"},
    'rarity_mythisch': {'de': "Mythisch", 'en': "Mythic"},

    # Game Data: Item Blueprints (example)
    'item_sword': {'de': "Schwert", 'en': "Sword"},
    'item_staff': {'de': "Stab", 'en': "Staff"},
    'item_dagger': {'de': "Dolch", 'en': "Dagger"},
    # ... more items would be added here

    # Game Data: Potions
    'potion_small_healing': {'de': "Kleiner Heiltrank", 'en': "Small Healing Potion"},
    'potion_healing': {'de': "Heiltrank", 'en': "Healing Potion"},
    'potion_large_healing': {'de': "Großer Heiltrank", 'en': "Large Healing Potion"},
    'potion_superior_healing': {'de': "Überragender Heiltrank", 'en': "Superior Healing Potion"},
    # ... other potions

    # Game Data: Bosses
    'boss_raging_boar': {'de': "Wütender Eber", 'en': "Raging Boar"},
    'boss_slime_king': {'de': "Schleimkönig", 'en': "Slime King"},

    # Game Data: Procedural Text
    'quest_location_forest': {'de': "in den düsteren Wäldern", 'en': "in the gloomy woods"},
    'quest_location_ruins': {'de': "zu den vergessenen Ruinen", 'en': "to the forgotten ruins"},
    'quest_location_desert': {'de': "durch die sengende Wüste", 'en': "through the scorching desert"},
    'quest_location_peaks': {'de': "über die eisigen Gipfel", 'en': "over the icy peaks"},
    'quest_location_mines': {'de': "tief in die Goblin-Minen", 'en': "deep into the goblin mines"},

    'quest_action_prefix_1': {'de': "Dort angekommen, musst du", 'en': "Once there, you must"},
    'quest_action_prefix_2': {'de': "Deine Aufgabe ist es,", 'en': "Your task is to"},
    'quest_action_prefix_3': {'de': "Im Zielgebiet angekommen, gilt es,", 'en': "Having reached the target area, you must"},

    'quest_return_1': {'de': "Nach getaner Arbeit machst du dich auf den Rückweg.", 'en': "With the work done, you start your journey back."},
    'quest_return_2': {'de': "Die Aufgabe ist erfüllt und du trittst die Heimreise an.", 'en': "The task is complete and you begin the journey home."},
    'quest_return_3': {'de': "Erschöpft, aber erfolgreich, beginnst du den Rückmarsch.", 'en': "Exhausted but successful, you begin the march back."},
    'quest_travel': {'de': "Deine Quest führt dich {location}.", 'en': "Your quest leads you {location}."},

    # Game Data: Quest Names
    'quest_kill_slimes': {'de': "Töte alle Schleime", 'en': "Kill all slimes"},
    'quest_bring_ore': {'de': "Bringe dem Schmied 5 Eisenerz", 'en': "Bring 5 iron ore to the blacksmith"},
    'quest_save_princess': {'de': "Rette eine Prinzessin aus einem anderen Schloss", 'en': "Save a princess from another castle"},
    'quest_collect_bottles': {'de': "Sammle 10 leere Flaschen für den Alchemisten", 'en': "Collect 10 empty bottles for the alchemist"},
    'quest_polish_armor': {'de': "Poliere die Rüstung des Königs (ohne Bezahlung)", 'en': "Polish the king's armor (unpaid)"},
    'quest_untangle_headphones': {'de': "Entwirre die Kopfhörer des Barden", 'en': "Untangle the bard's headphones"},
    'quest_find_recipe': {'de': "Finde das Rezept für ewige Jugend (und verliere es wieder)", 'en': "Find the recipe for eternal youth (and lose it again)"},
    'quest_teach_parrot': {'de': "Bringe dem königlichen Papagei das Fluchen bei", 'en': "Teach the royal parrot to curse"},
    'quest_count_sand': {'de': "Zähle alle Sandkörner am Strand", 'en': "Count all the grains of sand on the beach"},
    'quest_sort_library': {'de': "Sortiere die Bibliothek nach der Farbe der Buchrücken", 'en': "Sort the library by the color of the book spines"},
    'quest_convince_dragon': {'de': "Überzeuge einen Drachen, dass er nur ein überdimensionierter Wellensittich ist", 'en': "Convince a dragon he's just an oversized budgie"},
    'quest_find_goblin_mood': {'de': "Finde heraus, warum Goblins immer so schlechte Laune haben", 'en': "Find out why goblins are always in a bad mood"},
    'quest_escort_turtle': {'de': "Eskortiere eine sehr langsame Schildkröte über eine sehr breite Straße", 'en': "Escort a very slow turtle across a very wide road"},
    'quest_disrupt_ceremony': {'de': "Störe eine wichtige Zeremonie durch lautes Kauen", 'en': "Disrupt an important ceremony by chewing loudly"},

    # General UI & Actions
    'actions': {'de': "Aktionen", 'en': "Actions"},
    'character_status': {'de': "Charakterstatus", 'en': "Character Status"},
    'log': {'de': "Log", 'en': "Log"},
    'equipment': {'de': "Ausrüstung", 'en': "Equipment"},
    'inventory': {'de': "Inventar", 'en': "Inventory"},
    'start_new_quest': {'de': "Neue Quest beginnen", 'en': "Start New Quest"},
    'start_auto_quest': {'de': "Auto-Quest starten", 'en': "Start Auto-Quest"},
    'stop_auto_quest': {'de': "Auto-Quest stoppen", 'en': "Stop Auto-Quest"},
    'visit_trader': {'de': "Händler besuchen", 'en': "Visit Trader"},
    'visit_blacksmith': {'de': "Schmied besuchen", 'en': "Visit Blacksmith"},
    'visit_boss_arena': {'de': "Boss-Arena", 'en': "Boss Arena"},
    'equip_item': {'de': "Gegenstand ausrüsten", 'en': "Equip Item"},
    'use_item': {'de': "Gegenstand benutzen", 'en': "Use Item"},
    'resource_hunt': {'de': "Ressourcenjagd", 'en': "Resource Hunt"},

    # Character Stats
    'name': {'de': "Name:", 'en': "Name:"},
    'level': {'de': "Level:", 'en': "Level:"},
    'gold': {'de': "Gold:", 'en': "Gold:"},
    'attributes': {'de': "Attribute", 'en': "Attributes"},
    'strength': {'de': "Stärke", 'en': "Strength"},
    'agility': {'de': "Agilität", 'en': "Agility"},
    'intelligence': {'de': "Intelligenz", 'en': "Intelligence"},
    'luck': {'de': "Glück", 'en': "Luck"},
    'resources': {'de': "Ressourcen", 'en': "Resources"},
    'no_resources_collected': {'de': "Noch keine Ressourcen gesammelt.", 'en': "No resources collected yet."},
    'health_points': {'de': "Lebenspunkte", 'en': "Health Points"},
    'mana_points': {'de': "Manapunkte", 'en': "Mana Points"},
    'energy': {'de': "Energie", 'en': "Energy"},
    'rage': {'de': "Wut", 'en': "Rage"},
    'experience': {'de': "Erfahrung", 'en': "Experience"},

    # Equipment Slots
    'head': {'de': "Kopf", 'en': "Head"},
    'chest': {'de': "Brust", 'en': "Chest"},
    'weapon': {'de': "Waffe", 'en': "Weapon"},
    'empty_slot': {'de': "Leer", 'en': "Empty"},

    # Quest & Combat
    'quest_active_warning': {'de': "Quest aktiv", 'en': "Quest Active"},
    'quest_active_message': {'de': "Bitte schließe erst die aktuelle Quest ab.", 'en': "Please complete the current quest first."},
    'inventory_full_title': {'de': "Inventar voll", 'en': "Inventory Full"},
    'inventory_full_message': {'de': "Dein Inventar ist voll. Besuche den Händler!", 'en': "Your inventory is full. Visit the trader!"},
    'auto_quest_stopped_inventory': {'de': "Inventar voll! Auto-Quest gestoppt.", 'en': "Inventory full! Auto-Quest stopped."},
    'auto_quest_mode_active': {'de': "Auto-Quest Modus aktiv...", 'en': "Auto-Quest mode active..."},
    'auto_quest_mode_stopped': {'de': "Auto-Quest Modus gestoppt.", 'en': "Auto-Quest mode stopped."},
    'low_health_warning_title': {'de': "Niedrige Lebenspunkte!", 'en': "Low Health!"},
    'low_health_warning_message': {'de': "Deine Lebenspunkte sind kritisch niedrig! Auto-Quest pausiert. Heile dich!", 'en': "Your health is critically low! Auto-Quest paused. Heal up!"},
    'level_up_title': {'de': "Level Aufstieg!", 'en': "Level Up!"},
    'level_up_message': {'de': "Level Up! Du bist jetzt Level {level}!\n\nAttribut-Boni:\n{bonuses}", 'en': "Level Up! You are now level {level}!\n\nAttribute Bonuses:\n{bonuses}"},
    'loot_message': {'de': "Loot: {gold}, {xp} XP", 'en': "Loot: {gold}, {xp} XP"},
    'loot_with_item': {'de': " und '{item_name}'", 'en': " and '{item_name}'"},
    'loot_inventory_full': {'de': " (aber '{item_name}' passte nicht ins Inventar!)", 'en': " (but '{item_name}' did not fit into the inventory!)"},
}

def set_language(language_code):
    """
    Sets the global language for the application.

    Args:
        language_code (str): The language code ('de' or 'en').
    """
    global CURRENT_LANGUAGE
    if language_code in ['de', 'en']:
        CURRENT_LANGUAGE = language_code
    else:
        print(f"Warning: Language '{language_code}' not supported. Defaulting to 'en'.")
        CURRENT_LANGUAGE = 'en'

def get_text(key):
    """
    Retrieves a text string in the currently selected language.

    Args:
        key (str): The unique key for the text string.

    Returns:
        str: The translated text. Returns the key itself if not found.
    """
    if key in TEXTS:
        return TEXTS[key].get(CURRENT_LANGUAGE, TEXTS[key].get('en', key))
    return key
