# highscore_gui.py
"""
Defines the GUI window for displaying high scores.
"""
import tkinter as tk
from tkinter import ttk
from highscore_manager import load_highscores
from utils import center_window, format_currency

class HighscoreWindow(tk.Toplevel):
    """A Toplevel window to display the high score list."""

    def __init__(self, parent):
        """Initializes the high score window."""
        super().__init__(parent)
        self.title("Halle der Helden")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.populate_scores()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def create_widgets(self):
        """Creates and places the widgets for the window."""
        container = ttk.Frame(self, padding="10")
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Define the columns for the Treeview
        columns = ("name", "level", "best_equipment", "copper")
        self.tree = ttk.Treeview(container, columns=columns, show="headings")

        # Define headings
        self.tree.heading("name", text="Name")
        self.tree.heading("level", text="Level")
        self.tree.heading("best_equipment", text="Beste Ausrüstung")
        self.tree.heading("copper", text="Gold")

        # Configure column widths
        self.tree.column("name", width=120)
        self.tree.column("level", width=50, anchor="center")
        self.tree.column("best_equipment", width=300)
        self.tree.column("copper", width=100, anchor="e")

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Close button
        close_button = ttk.Button(container, text="Schließen", command=self.destroy)
        close_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        self.after(10, lambda: center_window(self))

    def populate_scores(self):
        """Loads scores and inserts them into the Treeview."""
        scores = load_highscores()
        for score in scores:
            copper_formatted = format_currency(score.get("copper", 0))
            best_equipment = (
                f"Waffe: {score.get('best_weapon', 'N/A')}, "
                f"Kopf: {score.get('best_head', 'N/A')}, "
                f"Brust: {score.get('best_chest', 'N/A')}"
            )
            self.tree.insert("", tk.END, values=(
                score.get("name", ""),
                score.get("level", 0),
                best_equipment,
                copper_formatted
            ))
