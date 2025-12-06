# boss.py
"""
Defines the Boss class for the RPG game.
"""
import random

class Boss:
    """Represents a boss enemy in the game."""

    def __init__(self, name, hp, damage_range, image_path, item_level=1, run_counter=0):
        self.name = name
        self.image_path = image_path
        self.is_weakened = False
        boss_scaling_reduction = max(0.80, 1.0 - 0.02 * run_counter)  # Minimal 80%, -2% pro Run
        scaling_factor = (1 + (item_level / 10) ** 1.2) * boss_scaling_reduction

        self.max_hp = int(hp * scaling_factor)
        self.current_hp = self.max_hp
        min_dmg, max_dmg = damage_range
        self.damage_range = (int(min_dmg * scaling_factor), int(max_dmg * scaling_factor))

    def attack(self):
        """
        Calculates the damage for the boss's attack.

        Returns:
            int: The amount of damage dealt.
        """
        return random.randint(*self.damage_range)

    def take_damage(self, damage):
        """
        Reduces the boss's HP by a given amount.
        If the boss is weakened, it takes increased damage.
        """
        final_damage = damage
        if self.is_weakened:
            final_damage = int(final_damage * 1.5)  # Take 50% more damage

        self.current_hp -= final_damage
        if self.current_hp < 0:
            self.current_hp = 0

    def is_defeated(self):
        """
        Checks if the boss has been defeated.

        Returns:
            bool: True if the boss's HP is 0, False otherwise.
        """
        return self.current_hp <= 0

