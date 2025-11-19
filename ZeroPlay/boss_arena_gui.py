# boss_arena_gui.py
"""
Defines the GUI for the boss arena.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
from PIL import Image, ImageTk

from boss import Boss
from game_data import AVAILABLE_BOSSES, CLASSES
from utils import center_window

class BossArenaWindow(tk.Toplevel):
    """A Toplevel window for the boss fight."""

    def __init__(self, parent, player, on_close_callback=None):
        """Initializes the boss arena window."""
        super().__init__(parent)
        self.title("Boss Arena")
        self.parent = parent
        self.player = player
        self.on_close_callback = on_close_callback

        # Prevent the user from interacting with the main window
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Select a random boss
        boss_data = random.choice(AVAILABLE_BOSSES)
        self.boss = Boss(
            name=boss_data["name"],
            hp=boss_data["hp"],
            damage_range=boss_data["damage"],
            image_path=boss_data["image_path"]
        )

        self.is_player_turn = True
        self.is_fight_over = False
        self._setup_string_vars()
        self.create_widgets()
        self.update_display()

        center_window(self, self.parent.winfo_toplevel())

    def _setup_string_vars(self):
        """Initializes StringVars for dynamic labels."""
        self.player_hp_var = tk.StringVar()
        self.boss_hp_var = tk.StringVar()
        self.player_name_var = tk.StringVar()
        self.boss_name_var = tk.StringVar()

    def create_widgets(self):
        """Creates and places all widgets for the arena."""
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        self.load_images()

    def load_images(self):
        """Loads images for player and boss."""
        try:
            player_img = Image.open(self.player.image_path)
            player_img.thumbnail((150, 200))
            self.player_photo = ImageTk.PhotoImage(player_img)
            self.player_portrait_label.config(image=self.player_photo)
        except Exception as e:
            self.player_portrait_label.config(text=f"Bildfehler:\n{e}")

        try:
            boss_img = Image.open(self.boss.image_path)
            boss_img.thumbnail((150, 200))
            self.boss_photo = ImageTk.PhotoImage(boss_img)
            self.boss_portrait_label.config(image=self.boss_photo)
        except Exception as e:
            self.boss_portrait_label.config(text=f"Bildfehler:\n{e}")

    def update_display(self):
        """Updates all dynamic widgets."""
        # Names
        self.player_name_var.set(f"{self.player.name} (Level {self.player.level})")
        self.boss_name_var.set(self.boss.name)

        # HP Bars and Labels
        self.player_hp_var.set(f"{self.player.current_lp} / {self.player.max_lp} LP")
        self.player_hp_bar['value'] = (self.player.current_lp / self.player.max_lp) * 100
        self.boss_hp_var.set(f"{self.boss.current_hp} / {self.boss.max_hp} HP")
        self.boss_hp_bar['value'] = (self.boss.current_hp / self.boss.max_hp) * 100

        # Buttons

    def add_to_log(self, message):
        """Adds a message to the combat log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def player_defend(self):
        """Handles the player's defend action."""
        if not self.is_player_turn or self.is_fight_over:
            return

        self.is_defending = True
        self.add_to_log("Du gehst in Verteidigungshaltung. Du erleidest halben Schaden durch den nächsten Angriff.")

        self.is_player_turn = False
        self.update_display()
        self.after(1000, self.boss_turn)

    def player_attack(self):
        """Handles the player's attack action."""
        if not self.is_player_turn or self.is_fight_over:
            return

        # Defensive check for main_stat, especially for characters from old save files
        if not hasattr(self.player, 'main_stat') or not self.player.main_stat:
            self.player.main_stat = CLASSES.get(self.player.klasse, {}).get("main_stat")

        player_stats = self.player.get_total_stats()
        main_stat = self.player.main_stat

        # Final check to prevent a crash if main_stat is still not found
        if not main_stat or main_stat not in player_stats:
            self.add_to_log(f"Fehler: Hauptattribut '{main_stat}' für Klasse '{self.player.klasse}' nicht gefunden!")
            messagebox.showerror("Kritischer Fehler", "Konnte das Hauptattribut des Charakters nicht bestimmen. Kampf wird abgebrochen.", parent=self)
            self.on_close()
            return

        player_damage = random.randint(player_stats[main_stat] // 2, player_stats[main_stat])

        self.boss.take_damage(player_damage)
        self.add_to_log(f"Du greifst an und verursachst {player_damage} Schaden bei {self.boss.name}!")
        self.update_display()

        if self.boss.is_defeated():
            self.end_fight(win=True)
        else:
            self.is_player_turn = False
            self.update_display()
            self.after(1000, self.boss_turn) # Boss attacks after a delay

    def boss_turn(self):
        """Handles the boss's turn to attack."""
        if self.is_fight_over:
            return

        boss_damage = self.boss.attack()

        if self.is_defending:
            boss_damage //= 2 # Halve the damage
            self.add_to_log(f"Deine Verteidigung halbiert den Schaden auf {boss_damage}!")
            self.is_defending = False # Reset defense state

        self.player.take_damage(boss_damage)
        self.add_to_log(f"{self.boss.name} greift an und fügt dir {boss_damage} Schaden zu!")
        self.update_display()

        if self.player.current_lp <= 0:
            self.end_fight(win=False)
        else:
            self.is_player_turn = True
            self.update_display()

    def end_fight(self, win):
        """Ends the fight and shows a result message."""
        self.is_fight_over = True
        self.attack_button.config(state=tk.DISABLED)
        self.defend_button.config(state=tk.DISABLED)

        if win:
            self.add_to_log(f"Du hast {self.boss.name} besiegt!")
            # Simple reward for winning
            gold_reward = self.boss.max_hp * 2
            xp_reward = self.boss.max_hp * 5
            self.player.add_loot(gold_reward, None)
            level_up_info = self.player.add_xp(xp_reward)

            message = f"Du hast gewonnen!\n\nBelohnung:\n{gold_reward} Gold\n{xp_reward} XP"
            if level_up_info:
                message += "\n\nLEVEL UP!"

            messagebox.showinfo("Sieg!", message, parent=self)
        else:
            self.add_to_log("Du wurdest besiegt...")
            # Let the main game loop handle the game over state
            messagebox.showerror("Niederlage", "Du hast den Kampf verloren!", parent=self)

        self.on_close()

    def on_close(self):
        """Handles the window closing event."""
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
