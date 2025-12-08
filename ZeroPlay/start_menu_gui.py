# start_menu_gui.py
"""
Defines the GUI Frame for the main start menu.
"""
import tkinter as tk
from tkinter import ttk
from save_load_system import get_save_files, load_game
from utils import format_currency
from localization import set_language, get_text

class StartMenu(ttk.Frame):
    """Manages the start menu frame."""

    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks # e.g., {'load': on_load, 'new': on_new, 'quit': on_quit}
        self.selected_save = None
        self.create_widgets()

    def _set_language_and_redraw(self, lang_code):
        """Sets the language and redraws the entire frame."""
        set_language(lang_code)
        # Destroy all current widgets
        for widget in self.winfo_children():
            widget.destroy()
        # Re-create all widgets with the new language
        self.create_widgets()

    def create_widgets(self):
        """Creates and places all widgets for the start menu."""
        self.master.title(get_text('main_menu_title'))

        # --- Language Selection ---
        lang_frame = ttk.Frame(self)
        lang_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT, padx=(0, 5))
        de_button = ttk.Button(lang_frame, text="Deutsch", command=lambda: self._set_language_and_redraw('de'))
        de_button.pack(side=tk.LEFT)
        en_button = ttk.Button(lang_frame, text="English", command=lambda: self._set_language_and_redraw('en'))
        en_button.pack(side=tk.LEFT, padx=5)

        # --- Introduction Text ---
        intro_text_content = get_text('intro_text')
        intro_frame = ttk.LabelFrame(self, text=get_text('instructions_title'), padding=10)
        intro_frame.pack(fill=tk.X, padx=10, pady=10)
        intro_label = ttk.Label(intro_frame, text=intro_text_content, wraplength=550, justify=tk.LEFT)
        intro_label.pack()

        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Left side: Save file list ---
        list_frame = ttk.Frame(main_pane, padding=5)
        main_pane.add(list_frame, weight=1)
        ttk.Label(list_frame, text=get_text('available_saves_label'), font=("Helvetica", 12)).pack(pady=5)
        self.save_listbox = tk.Listbox(list_frame)
        self.save_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.save_listbox.yview)
        self.save_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.populate_save_list()
        self.save_listbox.bind('<<ListboxSelect>>', self.on_select)

        # --- Right side: Character Preview ---
        self.preview_frame = ttk.LabelFrame(main_pane, text=get_text('preview_title'), padding=10)
        main_pane.add(self.preview_frame, weight=1)
        self._create_preview_widgets(self.preview_frame)

        # --- Bottom buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

        self.load_button = ttk.Button(button_frame, text=get_text('load_button'), command=self.load_game, state=tk.DISABLED)
        self.load_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        new_game_button = ttk.Button(button_frame, text=get_text('new_game_button'), command=self.callbacks['new'])
        new_game_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        highscore_button = ttk.Button(button_frame, text=get_text('highscores_button'), command=self.callbacks.get('highscores', lambda: None))
        highscore_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        quit_button = ttk.Button(button_frame, text=get_text('quit_button'), command=self.callbacks['quit'])
        quit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.clear_preview() # Initialize with default text

    def _create_preview_widgets(self, parent):
        """Creates the widgets for the character preview area."""
        self.preview_name_var = tk.StringVar()
        self.preview_level_var = tk.StringVar()
        self.preview_gold_var = tk.StringVar()
        self.preview_stats_vars = {
            'Stärke': tk.StringVar(),
            'Intelligenz': tk.StringVar(),
            'Glück': tk.StringVar(),
        }

        ttk.Label(parent, textvariable=self.preview_name_var).pack(anchor=tk.W)
        ttk.Label(parent, textvariable=self.preview_level_var).pack(anchor=tk.W)
        ttk.Label(parent, textvariable=self.preview_gold_var).pack(anchor=tk.W, pady=(0, 10))

        for stat_key in self.preview_stats_vars:
            ttk.Label(parent, textvariable=self.preview_stats_vars[stat_key]).pack(anchor=tk.W)

    def populate_save_list(self):
        """Fills the listbox with available save files."""
        self.save_listbox.delete(0, tk.END)
        for save_name in get_save_files():
            self.save_listbox.insert(tk.END, save_name)

    def on_select(self, event=None):
        """Loads character data and displays it in the preview."""
        if not self.save_listbox.curselection():
            self.load_button.config(state=tk.DISABLED)
            self.selected_save = None
            self.clear_preview()
            return

        self.load_button.config(state=tk.NORMAL)
        self.selected_save = self.save_listbox.get(self.save_listbox.curselection())

        char = load_game(self.selected_save)
        if char:
            self.preview_name_var.set(f"{get_text('name_label')} {char.name} ({char.klasse})")
            self.preview_level_var.set(f"{get_text('level_label')} {char.level}")
            self.preview_gold_var.set(f"{get_text('gold_label')} {format_currency(char.copper)}")
            for stat_key, var in self.preview_stats_vars.items():
                var.set(f"{get_text(stat_key.lower())}: {char.attributes.get(stat_key, 0)}")
        else:
            self.clear_preview()

    def clear_preview(self):
        """Resets the preview labels to their default (translated) state."""
        self.preview_name_var.set(f"{get_text('name_label')} -")
        self.preview_level_var.set(f"{get_text('level_label')} -")
        self.preview_gold_var.set(f"{get_text('gold_label')} -")
        for stat_key, var in self.preview_stats_vars.items():
            var.set(f"{get_text(stat_key.lower())}: -")

    def load_game(self):
        if self.selected_save and self.callbacks['load']:
            self.callbacks['load'](self.selected_save)
