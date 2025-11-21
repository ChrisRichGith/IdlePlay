# boss_arena_gui.py
"""
Defines the GUI for the boss arena.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
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
        self.player_is_empowered = False
        self.is_defending = False
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
        # Main container frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1, uniform="group1")
        main_frame.columnconfigure(1, weight=2, uniform="group1") # Log in the middle
        main_frame.columnconfigure(2, weight=1, uniform="group1")
        main_frame.rowconfigure(0, weight=1)

        # --- Player Frame (Left) ---
        player_frame = ttk.LabelFrame(main_frame, text="Spieler", padding="10")
        player_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        player_frame.columnconfigure(0, weight=1)
        player_frame.rowconfigure(1, weight=1) # Make portrait area expand

        ttk.Label(player_frame, textvariable=self.player_name_var).pack(pady=5)
        self.player_portrait_label = ttk.Label(player_frame)
        self.player_portrait_label.pack(pady=5, expand=True)
        ttk.Label(player_frame, textvariable=self.player_hp_var).pack()
        self.player_hp_bar = ttk.Progressbar(player_frame, orient='horizontal', mode='determinate')
        self.player_hp_bar.pack(fill=tk.X, padx=5, pady=5)


        # --- Middle Frame (Log and Actions) ---
        middle_frame = ttk.Frame(main_frame)
        middle_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        middle_frame.rowconfigure(0, weight=3) # Log gets more space
        middle_frame.rowconfigure(1, weight=1) # Actions
        middle_frame.columnconfigure(0, weight=1)

        # Combat Log
        log_frame = ttk.LabelFrame(middle_frame, text="Kampflog", padding="5")
        log_frame.grid(row=0, column=0, sticky="nsew")
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD, bg="#2B2B2B", fg="white", relief="flat")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(state=tk.DISABLED)
        self.add_to_log(f"Ein wilder {self.boss.name} erscheint!")

        # Action Buttons
        actions_frame = ttk.LabelFrame(middle_frame, text="Aktionen", padding="10")
        actions_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        self.attack_button = ttk.Button(actions_frame, text="Angreifen", command=self.player_attack)
        self.attack_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.defend_button = ttk.Button(actions_frame, text="Verteidigen", command=self.player_defend)
        self.defend_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Dice label for animation (initially hidden)
        self.dice_label = ttk.Label(self, text="🎲", font=("", 36))


        # --- Boss Frame (Right) ---
        boss_frame = ttk.LabelFrame(main_frame, text="Boss", padding="10")
        boss_frame.grid(row=0, column=2, sticky="nsew", padx=5)
        boss_frame.columnconfigure(0, weight=1)
        boss_frame.rowconfigure(1, weight=1) # Make portrait area expand

        ttk.Label(boss_frame, textvariable=self.boss_name_var).pack(pady=5)
        self.boss_portrait_label = ttk.Label(boss_frame)
        self.boss_portrait_label.pack(pady=5, expand=True)
        ttk.Label(boss_frame, textvariable=self.boss_hp_var).pack()
        self.boss_hp_bar = ttk.Progressbar(boss_frame, orient='horizontal', mode='determinate')
        self.boss_hp_bar.pack(fill=tk.X, padx=5, pady=5)

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
        self.defend_button.config(state=tk.NORMAL if self.is_player_turn and not self.is_fight_over else tk.DISABLED)

    def add_to_log(self, message):
        """Adds a message to the combat log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _animate_dice_roll(self, roll, callback):
        """Animates a dice emoji with a zoom effect."""
        self.dice_label.config(text="🎲", font=("", 1))
        self.dice_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        start_time = time.time()
        duration = 0.3  # 300ms for zoom-in

        def zoom_step():
            elapsed = time.time() - start_time
            progress = min(elapsed / duration, 1.0)

            # Animate font size from 1 to 72
            font_size = int(1 + progress * 71)
            self.dice_label.config(font=("", font_size))

            if progress < 1.0:
                self.after(15, zoom_step)
            else:
                # After zoom, hide dice, show number, then call callback
                self.dice_label.place_forget()
                self.dice_label.config(text=f"{roll}", font=("", 48))
                self.dice_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                self.after(700, lambda: (self.dice_label.place_forget(), callback()))

        zoom_step()

    def player_defend(self):
        """Handles the player's defend action with a random dice roll effect."""
        if not self.is_player_turn or self.is_fight_over:
            return

        self.is_player_turn = False
        self.is_defending = True  # Always take half damage when defending
        self.update_display()

        roll = random.randint(1, 4)

        def handle_roll_result():
            self.add_to_log(f"Du verteidigst dich und würfelst eine {roll}!")
            if roll == 1:
                # 1. Counter-attack
                counter_damage = self.player.get_total_stats()[self.player.main_stat] // 4
                self.add_to_log(f"Konterangriff! Du fügst dem Boss {counter_damage} Schaden zu.")
                self.boss.take_damage(counter_damage)
            elif roll == 2:
                # 2. Empowered next attack
                self.player_is_empowered = True
                self.add_to_log("Dein nächster Angriff wird verstärkt!")
            elif roll == 3:
                # 3. Light heal
                heal_amount = self.player.max_lp // 10  # Heal for 10% of max HP
                self.player.current_lp = min(self.player.max_lp, self.player.current_lp + heal_amount)
                self.add_to_log(f"Leichte Heilung! Du regenerierst {heal_amount} Lebenspunkte.")
            elif roll == 4:
                # 4. Weaken the boss
                self.boss.is_weakened = True
                self.add_to_log(f"{self.boss.name} ist für eine Runde geschwächt!")

            self.after(1000, self.boss_turn)

        self._animate_dice_roll(roll, handle_roll_result)

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

        if self.boss.is_weakened:
            self.add_to_log(f"{self.boss.name} ist geschwächt und erleidet mehr Schaden!")
            self.boss.is_weakened = False

        player_damage = random.randint(player_stats[main_stat] // 2, player_stats[main_stat])

        if self.player_is_empowered:
            player_damage = int(player_damage * 1.5)
            self.add_to_log("Verstärkter Angriff!")
            self.player_is_empowered = False

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
