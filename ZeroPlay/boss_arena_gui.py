# boss_arena_gui.py
"""
Defines the GUI for the Boss Arena feature.
"""
import tkinter as tk
from tkinter import ttk
import copy

from game_data import AVAILABLE_BOSSES
from utils import center_window
from localization import get_text

class BossArenaWindow(tk.Toplevel):
    """Manages the Boss Arena window."""

    def __init__(self, parent, player, on_close_callback=None):
        """Initializes the Boss Arena window."""
        super().__init__(parent)
        self.title(get_text('boss_arena_title'))
        self.transient(parent)
        self.grab_set()

        self.player = player
        self.on_close_callback = on_close_callback

        self.bosses = copy.deepcopy(AVAILABLE_BOSSES)
        self.selected_boss = None

        self._configure_styles()
        self._create_widgets()

        center_window(self, parent.winfo_toplevel())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _configure_styles(self):
        """Configures custom ttk styles for buttons."""
        style = ttk.Style(self)
        style.configure("Red.TButton", background="red", foreground="white", font=('Helvetica', '9', 'bold'))
        style.map("Red.TButton", background=[('active', '#FF4C4C')])
        style.configure("Yellow.TButton", background="orange", foreground="black", font=('Helvetica', '9', 'bold'))
        style.map("Yellow.TButton", background=[('active', '#FFC74C')])
        style.configure("Green.TButton", background="green", foreground="white", font=('Helvetica', '9', 'bold'))
        style.map("Green.TButton", background=[('active', '#4CFF4C')])

    def _create_widgets(self):
        """Creates and places all the widgets for the arena."""
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        selection_frame = ttk.LabelFrame(self, text=get_text('choose_opponent_label'), padding=10)
        selection_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.boss_listbox = tk.Listbox(selection_frame, bg="#2B2B2B", fg="white", selectbackground="#0078D7", height=15)
        for boss in self.bosses:
            self.boss_listbox.insert(tk.END, boss.name)
        self.boss_listbox.pack(fill=tk.Y, expand=True)
        self.boss_listbox.bind('<<ListboxSelect>>', self._on_boss_select)

        combat_frame = ttk.LabelFrame(self, text=get_text('fight_title'), padding=10)
        combat_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        combat_frame.columnconfigure(0, weight=1)
        combat_frame.rowconfigure(2, weight=1)

        player_stats_frame = ttk.Frame(combat_frame)
        player_stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        player_stats_frame.columnconfigure(1, weight=1)
        ttk.Label(player_stats_frame, text=f"{self.player.name}", font=("", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.player_hp_bar = ttk.Progressbar(player_stats_frame, orient='horizontal', mode='determinate')
        self.player_hp_bar.grid(row=0, column=1, sticky="ew", padx=5)
        self.player_hp_label = ttk.Label(player_stats_frame, text="")
        self.player_hp_label.grid(row=0, column=2, sticky="e")
        self._update_player_hp()

        boss_stats_frame = ttk.Frame(combat_frame)
        boss_stats_frame.grid(row=1, column=0, sticky="ew")
        boss_stats_frame.columnconfigure(1, weight=1)
        self.boss_name_label = ttk.Label(boss_stats_frame, text="---", font=("", 10, "bold"))
        self.boss_name_label.grid(row=0, column=0, sticky="w")
        self.boss_hp_bar = ttk.Progressbar(boss_stats_frame, orient='horizontal', mode='determinate')
        self.boss_hp_bar.grid(row=0, column=1, sticky="ew", padx=5)
        self.boss_hp_label = ttk.Label(boss_stats_frame, text="")
        self.boss_hp_label.grid(row=0, column=2, sticky="e")

        log_frame = ttk.Frame(combat_frame)
        log_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.combat_log = tk.Text(log_frame, height=10, wrap=tk.WORD, bg="#2B2B2B", fg="white", relief="flat", state=tk.DISABLED)
        self.combat_log.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.combat_log.yview)
        self.combat_log.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        action_frame = ttk.LabelFrame(self, text=get_text('actions'), padding=10)
        action_frame.grid(row=0, column=2, sticky="ns", padx=(0, 10), pady=10)

        self.fight_button = ttk.Button(action_frame, text=get_text('start_fight_button'), command=self._start_fight, state=tk.DISABLED)
        self.fight_button.pack(fill=tk.X, pady=5)

        ttk.Separator(action_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        self.attack_button = ttk.Button(action_frame, text=get_text('attack_button'), command=self._player_attack, state=tk.DISABLED)
        self.attack_button.pack(fill=tk.X, pady=5)
        self.potion_button = ttk.Button(action_frame, text=get_text('use_potion_button'), command=self._use_potion, state=tk.DISABLED)
        self.potion_button.pack(fill=tk.X, pady=5)
        self.flee_button = ttk.Button(action_frame, text=get_text('flee_button'), command=self._flee, state=tk.DISABLED)
        self.flee_button.pack(fill=tk.X, pady=5)

    def _update_player_hp(self):
        self.player_hp_bar['value'] = (self.player.current_lp / self.player.max_lp) * 100
        self.player_hp_label.config(text=f"{self.player.current_lp}/{self.player.max_lp} LP")

    def _update_boss_hp(self):
        if self.selected_boss:
            self.boss_hp_bar['value'] = (self.selected_boss.current_hp / self.selected_boss.max_hp) * 100
            self.boss_hp_label.config(text=f"{self.selected_boss.current_hp}/{self.selected_boss.max_hp} LP")
        else:
            self.boss_hp_bar['value'] = 0
            self.boss_hp_label.config(text="")

    def _on_boss_select(self, event=None):
        selected_indices = self.boss_listbox.curselection()
        if not selected_indices:
            return

        self.selected_boss = self.bosses[selected_indices[0]]
        self.boss_name_label.config(text=self.selected_boss.name)
        self._update_boss_hp()
        self._update_fight_button_state()

    def _update_fight_button_state(self):
        if not self.selected_boss:
            self.fight_button.config(state=tk.DISABLED)
            return

        player_main_stat = self.player.get_total_stats().get(self.player.main_stat, 0)
        player_power = player_main_stat + self.player.level
        boss_power = self.selected_boss.attack + self.selected_boss.defense
        ratio = player_power / boss_power if boss_power > 0 else 100

        style = "Green.TButton"
        if ratio < 0.8: style = "Red.TButton"
        elif ratio < 1.2: style = "Yellow.TButton"
        self.fight_button.config(style=style, state=tk.NORMAL)

    def _add_to_log(self, message):
        self.combat_log.config(state=tk.NORMAL)
        self.combat_log.insert(tk.END, message + "\n")
        self.combat_log.see(tk.END)
        self.combat_log.config(state=tk.DISABLED)

    def _start_fight(self):
        self._add_to_log(get_text('fight_begins_log').format(boss_name=self.selected_boss.name))
        self.fight_button.config(state=tk.DISABLED)
        self.boss_listbox.config(state=tk.DISABLED)
        self.attack_button.config(state=tk.NORMAL)
        self.potion_button.config(state=tk.NORMAL)
        self.flee_button.config(state=tk.NORMAL)

    def _player_attack(self):
        player_stats = self.player.get_total_stats()
        player_attack = player_stats.get(self.player.main_stat, 0)
        damage = max(1, player_attack - self.selected_boss.defense)

        self.selected_boss.take_damage(damage)
        self._add_to_log(get_text('player_attack_log').format(boss_name=self.selected_boss.name, damage=damage))
        self._update_boss_hp()

        if self.selected_boss.is_defeated():
            self._handle_victory()
        else:
            self.after(500, self._boss_attack)

    def _boss_attack(self):
        player_main_stat = self.player.get_total_stats().get(self.player.main_stat, 0)
        player_defense = int(player_main_stat / 2)
        damage = max(1, self.selected_boss.attack - player_defense)

        self.player.current_lp -= damage
        if self.player.current_lp < 0: self.player.current_lp = 0
        self._add_to_log(get_text('boss_attack_log').format(boss_name=self.selected_boss.name, damage=damage))
        self._update_player_hp()

        if self.player.current_lp <= 0:
            self._handle_defeat()

    def _use_potion(self):
        potion_to_use, item_index = None, -1
        for i, item in enumerate(self.player.inventory):
            if item.item_type == "Verbrauchsgut" and item.attributes.get("type") == "LP":
                potion_to_use, item_index = item, i
                break

        if potion_to_use:
            success, message = self.player.use_item(item_index)
            self._add_to_log(get_text(message))
            if success:
                self._update_player_hp()
                self.after(500, self._boss_attack)
        else:
            self._add_to_log(get_text('no_potions_log'))

    def _flee(self):
        self._add_to_log(get_text('fled_log'))
        self.on_close()

    def _handle_victory(self):
        self._add_to_log(get_text('victory_log').format(boss_name=self.selected_boss.name))

        self.attack_button.config(state=tk.DISABLED)
        self.potion_button.config(state=tk.DISABLED)
        self.flee_button.config(state=tk.DISABLED)

        reward = self.selected_boss.reward
        xp_gain, copper_gain, items = reward.get('xp', 0), reward.get('copper', 0), reward.get('items', [])

        self.player.copper += copper_gain
        level_up_info = self.player.add_xp(xp_gain)

        loot_messages = [get_text('loot_xp_log').format(xp=xp_gain), get_text('loot_copper_log').format(copper=copper_gain)]

        for item in items:
            if item and self.player.add_item_to_inventory(item):
                loot_messages.append(get_text('loot_item_log').format(item_name=item.name))
            elif item:
                loot_messages.append(get_text('loot_inventory_full_log').format(item_name=item.name))

        self._add_to_log(get_text('rewards_log_header'))
        for msg in loot_messages: self._add_to_log(msg)

        if level_up_info:
            self._add_to_log(get_text('level_up_log_header'))
            for info in level_up_info: self._add_to_log(info)

        self.after(3000, self.on_close)

    def _handle_defeat(self):
        self._add_to_log(get_text('defeat_log'))
        self.attack_button.config(state=tk.DISABLED)
        self.potion_button.config(state=tk.DISABLED)
        self.flee_button.config(state=tk.DISABLED)
        self.after(2000, self.on_close)

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
