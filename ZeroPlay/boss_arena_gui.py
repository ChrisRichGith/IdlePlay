# boss_arena_gui.py
"""
Defines the GUI for the boss arena.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
from PIL import Image, ImageTk

from boss import Boss
from game_data import AVAILABLE_BOSSES
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
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # --- Player Frame ---
        player_frame = ttk.LabelFrame(main_frame, text="Spieler", padding="10")
        player_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.player_portrait_label = ttk.Label(player_frame)
        self.player_portrait_label.pack()
        ttk.Label(player_frame, textvariable=self.player_name_var).pack(pady=5)
        self.player_hp_bar = ttk.Progressbar(player_frame, orient='horizontal', mode='determinate')
        self.player_hp_bar.pack(fill=tk.X, expand=True, pady=5)
        ttk.Label(player_frame, textvariable=self.player_hp_var).pack()

        # --- Boss Frame ---
        boss_frame = ttk.LabelFrame(main_frame, text="Boss", padding="10")
        boss_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.boss_portrait_label = ttk.Label(boss_frame)
        self.boss_portrait_label.pack()
        ttk.Label(boss_frame, textvariable=self.boss_name_var).pack(pady=5)
        self.boss_hp_bar = ttk.Progressbar(boss_frame, orient='horizontal', mode='determinate')
        self.boss_hp_bar.pack(fill=tk.X, expand=True, pady=5)
        ttk.Label(boss_frame, textvariable=self.boss_hp_var).pack()

        # --- Action Frame ---
        action_frame = ttk.LabelFrame(main_frame, text="Aktionen", padding="10")
        action_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        self.attack_button = ttk.Button(action_frame, text="Angriff", command=self.player_attack)
        self.attack_button.grid(row=0, column=0, padx=5, sticky="ew")
        self.defend_button = ttk.Button(action_frame, text="Verteidigen (nicht impl.)", state=tk.DISABLED)
        self.defend_button.grid(row=0, column=1, padx=5, sticky="ew")

        # --- Log Frame ---
        log_frame = ttk.LabelFrame(main_frame, text="Kampflog", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, state=tk.DISABLED, bg="#2B2B2B", fg="white")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Load images
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
        self.attack_button.config(state=tk.NORMAL if self.is_player_turn and not self.is_fight_over else tk.DISABLED)

    def add_to_log(self, message):
        """Adds a message to the combat log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def player_attack(self):
        """Handles the player's attack action."""
        if not self.is_player_turn or self.is_fight_over:
            return

        # Simple damage calculation
        player_stats = self.player.get_total_stats()
        main_stat = self.player.main_stat
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
            self.player.current_lp = 1 # Restore 1 HP to avoid game over
            messagebox.showerror("Niederlage", "Du hast den Kampf verloren!", parent=self)

        self.on_close()

    def on_close(self):
        """Handles the window closing event."""
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
