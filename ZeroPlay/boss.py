# boss.py
"""
Defines the Boss class for the RPG game.
"""
import random

class Boss:
    """Represents a boss enemy in the game."""

    def __init__(self, name, hp, damage_range, image_path):
        """
        Initializes a new Boss.

        Args:
            name (str): The name of the boss.
            hp (int): The maximum and current health points of the boss.
            damage_range (tuple): A tuple containing the min and max damage.
            image_path (str): The file path for the boss's image.
        """
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.damage_range = damage_range
        self.image_path = image_path
        self.is_weakened = False

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
