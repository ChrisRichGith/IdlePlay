# blacksmith_gui.py
"""
Defines the GUI for the Blacksmith.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from blacksmith import Blacksmith
from utils import center_window
from localization import get_text

class BlacksmithWindow(tk.Toplevel):
    """Manages the blacksmith interaction window."""

    def __init__(self, parent, player, on_close_callback):
        super().__init__(parent)
        self.title(get_text('blacksmith_title'))
        self.minsize(800, 600)
        self.transient(parent)
        self.grab_set()

        self.player = player
        self.blacksmith = Blacksmith()
        self.on_close_callback = on_close_callback
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.selected_item = None

        self.create_widgets()
        self.update_display()

        center_window(self, self.master.winfo_toplevel())

    def create_widgets(self):
        """Creates and places all widgets for the blacksmith window."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        equip_frame = ttk.LabelFrame(main_frame, text=get_text('equipment_title'), padding="10")
        equip_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        equip_frame.rowconfigure(0, weight=1)
        equip_frame.columnconfigure(0, weight=1)

        self.equip_listbox = tk.Listbox(equip_frame)
        self.equip_listbox.grid(row=0, column=0, sticky="nsew")
        self.equip_listbox.bind('<<ListboxSelect>>', self.on_item_select)

        details_frame = ttk.LabelFrame(main_frame, text=get_text('upgrade_title'), padding="10")
        details_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        self.item_name_label = ttk.Label(details_frame, text=get_text('select_item_prompt'), font=("", 12, "bold"))
        self.item_name_label.pack(pady=5)

        self.current_stats_label = ttk.Label(details_frame, text=get_text('current_stats_label'))
        self.current_stats_label.pack(pady=5, anchor="w")

        self.next_stats_label = ttk.Label(details_frame, text=get_text('next_level_label'))
        self.next_stats_label.pack(pady=5, anchor="w")

        self.cost_label = ttk.Label(details_frame, text=get_text('cost_label_blacksmith'))
        self.cost_label.pack(pady=10, anchor="w")

        self.upgrade_button = ttk.Button(details_frame, text=get_text('upgrade_button'), command=self.upgrade_item, state=tk.DISABLED)
        self.upgrade_button.pack(pady=20, fill=tk.X, ipady=5)

        self.player_resources_label = ttk.Label(details_frame, text=get_text('your_resources_label'))
        self.player_resources_label.pack(side=tk.BOTTOM, pady=10)

    def update_display(self):
        """Updates all displayed information."""
        self.equip_listbox.delete(0, tk.END)
        for slot, item in self.player.equipment.items():
            slot_name = get_text(slot.lower())
            if item:
                self.equip_listbox.insert(tk.END, f"[{slot_name}] {item.name}")
            else:
                self.equip_listbox.insert(tk.END, f"[{slot_name}] {get_text('empty_slot')}")

        resources_text = get_text('your_resources_label') + "\n" + "\n".join([f"{name}: {amount}" for name, amount in self.player.resources.items()])
        self.player_resources_label.config(text=resources_text)

        self.update_details()

    def on_item_select(self, event=None):
        """Handles the selection of an item in the listbox."""
        selected_indices = self.equip_listbox.curselection()
        if not selected_indices:
            self.selected_item = None
            return

        slot_order = ['Kopf', 'Brust', 'Waffe']
        selected_slot_name = slot_order[selected_indices[0]]
        self.selected_item = self.player.equipment.get(selected_slot_name)
        self.update_details()

    def update_details(self):
        """Updates the details section for the selected item."""
        if not self.selected_item:
            self.item_name_label.config(text=get_text('select_item_prompt'))
            self.current_stats_label.config(text=get_text('current_stats_label'))
            self.next_stats_label.config(text=get_text('next_level_label'))
            self.cost_label.config(text=get_text('cost_label_blacksmith'))
            self.upgrade_button.config(state=tk.DISABLED)
            return

        self.item_name_label.config(text=self.selected_item.name)

        stats_text = get_text('current_stats_label') + "\n" + "\n".join([f"  {get_text(stat.lower())}: {val}" for stat, val in self.selected_item.stats_boost.items()])
        self.current_stats_label.config(text=stats_text)

        next_level_stats = {stat: val + 1 for stat, val in self.selected_item.stats_boost.items()}
        next_stats_text = f"{get_text('next_level_label')} (+{self.selected_item.upgrade_level + 1}):\n" + "\n".join([f"  {get_text(stat.lower())}: {val}" for stat, val in next_level_stats.items()])
        self.next_stats_label.config(text=next_stats_text)

        cost = self.blacksmith.get_upgrade_cost(self.selected_item)
        if cost:
            cost_text = get_text('cost_label_blacksmith') + "\n" + "\n".join([f"  {name}: {amount}" for name, amount in cost.items()])
            self.cost_label.config(text=cost_text)
            if self.blacksmith.can_afford_upgrade(self.player.resources, cost):
                self.upgrade_button.config(state=tk.NORMAL)
            else:
                self.upgrade_button.config(state=tk.DISABLED)
        else:
            self.cost_label.config(text=f"{get_text('cost_label_blacksmith')} {get_text('max_level_reached')}")
            self.upgrade_button.config(state=tk.DISABLED)

    def upgrade_item(self):
        """Handles the item upgrade logic."""
        if not self.selected_item:
            return

        cost = self.blacksmith.get_upgrade_cost(self.selected_item)

        if not self.blacksmith.can_afford_upgrade(self.player.resources, cost):
            messagebox.showwarning(get_text('not_enough_resources_title'), get_text('not_enough_resources_message'), parent=self)
            return

        self.player.remove_resources(cost)
        self.selected_item.upgrade()
        messagebox.showinfo(get_text('upgrade_success_title_blacksmith'), get_text('upgrade_success_message_blacksmith').format(item_name=self.selected_item.name), parent=self)
        self.update_display()

    def on_close(self):
        """Called when the window is closed."""
        self.on_close_callback()
        self.destroy()
