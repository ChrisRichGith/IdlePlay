# loot_system.py
"""
Handles the dynamic generation of loot based on player level.
"""
import random
from item import Item
from game_data import ITEM_BLUEPRINTS, RARITIES

def generate_item_for_level(level, luck):
    """
    Generates a new item with stats, rarity, and value scaled to the given level.

    Args:
        level (int): The player's current level.
        luck (int): The player's luck attribute, influences rarity.

    Returns:
        Item: A newly generated Item object.
    """
    # 1. Choose a rarity based on level and luck
    available_rarities = {r: data for r, data in RARITIES.items() if level >= data["min_level"]}

    rarity_names = list(available_rarities.keys())
    rarity_weights = [data["weight"] for data in available_rarities.values()]

    # Luck increases the chance of finding better items
    luck_factor = 1 + (luck / 100) # 50 luck = 1.5x weight for better items
    for i, r_name in enumerate(rarity_names):
        if r_name not in ["Schlecht", "Gewöhnlich"]:
             rarity_weights[i] *= luck_factor

    chosen_rarity_name = random.choices(rarity_names, weights=rarity_weights, k=1)[0]
    rarity_data = RARITIES[chosen_rarity_name]

    # 2. Select a slot and a blueprint
    slot = random.choice(list(ITEM_BLUEPRINTS.keys()))
    blueprint = random.choice(ITEM_BLUEPRINTS[slot])

    # 3. Assemble the item name
    item_name = f"{chosen_rarity_name} {blueprint['name'][0]}"

    # 4. Calculate stat bonuses
    stats_boost = {}

    # Primary stat bonus calculation
    base_bonus = blueprint["base_bonus"]
    # Formula: Bonus scales with level and is modified by rarity
    primary_stat_value = int((base_bonus + (level * 0.9)) * rarity_data["modifier"])

    # Add some variance (+/- 5%) to create "+" versions implicitly
    primary_stat_value = int(primary_stat_value * random.uniform(0.95, 1.05))
    stats_boost[blueprint["base_stat"]] = max(1, primary_stat_value)

    # Add secondary stats for higher rarities
    all_stats = ["Stärke", "Agilität", "Intelligenz", "Glück"]
    if chosen_rarity_name in ["Episch", "Legendär", "Mythisch"]:
        possible_secondary_stats = [s for s in all_stats if s != blueprint["base_stat"]]
        if possible_secondary_stats:
            secondary_stat = random.choice(possible_secondary_stats)
            secondary_value = int(primary_stat_value * 0.4) # Secondary stat is 40% of primary
            stats_boost[secondary_stat] = max(1, secondary_value)

    if chosen_rarity_name == "Mythisch":
        # A third stat for mythisch items
        possible_tertiary_stats = [s for s in all_stats if s not in stats_boost]
        if possible_tertiary_stats:
            tertiary_stat = random.choice(possible_tertiary_stats)
            tertiary_value = int(primary_stat_value * 0.25) # Tertiary stat is 25% of primary
            stats_boost[tertiary_stat] = max(1, tertiary_value)

    # 5. Calculate item value
    total_stat_points = sum(stats_boost.values())
    value = int((level * 1.5) + (total_stat_points * 2.0) * rarity_data["modifier"])
    value = max(1, value)

    # Get armor type from blueprint if it exists
    armor_type = blueprint.get("armor_type")

    return Item(
        name=item_name,
        slot=slot,
        stats_boost=stats_boost,
        value=value,
        rarity=chosen_rarity_name,
        color=rarity_data["color"],
        armor_type=armor_type
    )


def generate_boss_reward(player):
    """
    Generates a guaranteed item upgrade for the player after defeating a boss.
    The item will be for a random slot and will be statistically better than
    what the player currently has equipped in that slot.

    Args:
        player (Character): The player character.

    Returns:
        Item: A powerful new Item object.
    """
    # 1. Choose a random slot to upgrade
    slots = ["Waffe", "Kopf", "Brust"]
    chosen_slot = random.choice(slots)

    # 2. Determine the rarity based on player level, ensuring it's at least "Selten"
    if player.level < 15:
        chosen_rarity_name = "Selten"
    elif player.level < 30:
        chosen_rarity_name = "Episch"
    else:
        chosen_rarity_name = "Legendär"
    rarity_data = RARITIES[chosen_rarity_name]

    # 3. Find a suitable blueprint for the player's class
    allowed_armor_types = player.get_allowed_armor_types()
    main_stat = player.main_stat

    possible_blueprints = [
        bp for bp in ITEM_BLUEPRINTS[chosen_slot]
        if (bp.get("armor_type") in allowed_armor_types and bp.get("base_stat") == main_stat)
        or (chosen_slot == "Waffe" and bp.get("base_stat") == main_stat)
    ]

    if not possible_blueprints:
        # Fallback: just pick a main-stat appropriate weapon if armor fails
        possible_blueprints = [bp for bp in ITEM_BLUEPRINTS["Waffe"] if bp.get("base_stat") == main_stat]
        chosen_slot = "Waffe"

    blueprint = random.choice(possible_blueprints)

    # 4. Generate stats that are a guaranteed upgrade
    # Get the currently equipped item's score to use as a baseline
    currently_equipped = player.equipment.get(chosen_slot)
    base_score = 0
    if currently_equipped:
        base_score = currently_equipped.get_weighted_score(main_stat)

    # Ensure the new item's primary stat is significantly better
    stats_boost = {}
    # Make the bonus at least 20% better than the current item's score
    # and also scale with level and rarity.
    min_primary_stat = int((base_score * 1.2) + (player.level * 1.5))
    primary_stat_value = int(min_primary_stat * rarity_data["modifier"])
    stats_boost[main_stat] = max(min_primary_stat, primary_stat_value)

    # Add a secondary stat (Luck or the main stat again for a bigger boost)
    if random.random() < 0.75: # 75% chance for more main stat
        stats_boost[main_stat] += int(primary_stat_value * 0.4)
    else:
        stats_boost["Glück"] = int(primary_stat_value * 0.5)

    # 5. Assemble the item
    item_name = f"Bosse {blueprint['name'][0]}"
    total_stat_points = sum(stats_boost.values())
    value = int((player.level * 5) + (total_stat_points * 4) * rarity_data["modifier"])
    armor_type = blueprint.get("armor_type")

    return Item(
        name=item_name,
        slot=chosen_slot,
        stats_boost=stats_boost,
        value=value,
        rarity=chosen_rarity_name,
        color=rarity_data["color"],
        armor_type=armor_type
    )


# Example usage for testing:
if __name__ == '__main__':
    for lvl in [1, 5, 10, 20, 50]:
        print(f"--- Generating Item for Level {lvl} ---")
        for _ in range(3):
            new_item = generate_item_for_level(lvl, 5)
            print(new_item)
        print("-" * 20)