
import tkinter as tk
import unittest
from unittest.mock import MagicMock
import sys
import os

# Add the ZeroPlay directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ZeroPlay')))

from rpg_gui import RpgGui
from character import Character

class TestRpgGui(unittest.TestCase):
    def test_quest_image_is_set(self):
        root = tk.Tk()
        # We don't want the window to actually appear
        root.withdraw()

        character = Character("TestPlayer", "Krieger")
        callbacks = {"game_over": MagicMock()}

        gui = RpgGui(root, character, callbacks)

        # Ensure the image label is initially empty
        self.assertIsNone(gui.quest_image_label.image)

        # Start a quest
        gui.start_quest()

        # Check if an image has been assigned to the label
        self.assertIsNotNone(gui.quest_image_label.image, "The quest image label was not updated after starting a quest.")

        # Clean up the tkinter window
        root.destroy()

if __name__ == '__main__':
    unittest.main()
