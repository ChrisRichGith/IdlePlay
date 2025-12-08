# boss.py
"""
Defines the Boss class for the RPG game.
"""

class Boss:
    """Represents a boss enemy in the game."""

    def __init__(self, name, max_hp, attack, defense, reward):
        """
        Initializes a new Boss instance.

        Args:
            name (str): The name of the boss.
            max_hp (int): The maximum health points of the boss.
            attack (int): The attack power of the boss.
            defense (int): The defense power of the boss.
            reward (dict): A dictionary containing the rewards for defeating the boss.
                           Expected keys: 'xp', 'copper', 'items' (list of Item objects or None).
        """
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.reward = reward

    def is_defeated(self):
        """Checks if the boss has been defeated."""
        return self.current_hp <= 0

    def take_damage(self, damage):
        """Reduces the boss's health by a given amount."""
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def __str__(self):
        """Returns the string representation of the boss."""
        return f"{self.name} (HP: {self.current_hp}/{self.max_hp})"
