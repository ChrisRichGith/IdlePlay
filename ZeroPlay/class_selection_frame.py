# class_selection_frame.py
"""
Defines the GUI Frame for the class selection scene.
"""
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
from game_data import CLASSES
from localization import get_text

class ClassSelectionFrame(ttk.Frame):
    """Manages the class selection frame."""

    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks # e.g., {'back': on_back, 'confirm': on_confirm}

        self.player_name = ""
        self.selected_class_key = "Krieger" # Default to the key

        self.create_widgets()

        # Set default selection and display its info
        self.class_var.set(self.selected_class_key)
        self.show_class_info()

    def create_widgets(self):
        """Creates the widgets for the class selection frame."""
        ttk.Label(self, text=get_text('create_character_title'), font=("Helvetica", 16)).pack(pady=20)

        # Name Entry
        name_frame = ttk.Frame(self)
        name_frame.pack(pady=10)
        ttk.Label(name_frame, text=get_text('hero_name_label')).pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT)

        # Main content frame
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)

        left_frame = ttk.Frame(content_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ttk.Label(left_frame, text=get_text('choose_your_class_label'), font=("Helvetica", 12)).pack(pady=(10, 10))
        self.class_var = tk.StringVar()
        class_options_frame = ttk.Frame(left_frame)
        class_options_frame.pack(anchor=tk.W)
        for class_key in CLASSES.keys():
            # Use translated class name for display
            rb = ttk.Radiobutton(class_options_frame, text=get_text(class_key.lower()), variable=self.class_var, value=class_key, command=self.show_class_info)
            rb.pack(anchor=tk.W, pady=2)

        self.info_frame = ttk.LabelFrame(left_frame, text=get_text('class_info_title'), padding="10", height=150)
        self.info_frame.pack(fill=tk.X, expand=True, pady=(20, 10))
        self.info_frame.pack_propagate(False)
        self.desc_label = ttk.Label(self.info_frame, text="", wraplength=380)
        self.desc_label.pack(anchor=tk.W, pady=5)
        self.attr_label = ttk.Label(self.info_frame, text="", font=("Courier", 10))
        self.attr_label.pack(anchor=tk.W, pady=5)

        right_frame = ttk.Frame(content_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.image_label = ttk.Label(right_frame, text=get_text('select_a_class_label'), anchor=tk.CENTER)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.character_photo = None

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

        self.confirm_button = ttk.Button(button_frame, text=get_text('start_adventure_button'), command=self.confirm, state=tk.DISABLED)
        self.confirm_button.pack(side=tk.RIGHT)

        back_button = ttk.Button(button_frame, text=get_text('back_to_main_menu_button'), command=self.callbacks['back'])
        back_button.pack(side=tk.RIGHT, padx=(0, 10))

    def show_class_info(self):
        """Displays information about the selected class."""
        self.selected_class_key = self.class_var.get()
        if self.selected_class_key:
            class_data = CLASSES[self.selected_class_key]
            self.desc_label.config(text=get_text(class_data["description_key"]))
            attr_text = get_text('start_attributes_label') + "\n"
            for stat, value in class_data["attributes"].items():
                attr_text += f"  - {get_text(stat.lower()):<12}: {value}\n"
            self.attr_label.config(text=attr_text)
            self.confirm_button.config(state=tk.NORMAL)

            try:
                img_path = class_data.get("image_path")
                if img_path:
                    img = Image.open(img_path)
                    img.thumbnail((300, 400))
                    self.character_photo = ImageTk.PhotoImage(img)
                    self.image_label.config(image=self.character_photo, text="")
                else:
                    self.image_label.config(image="", text=get_text('no_image_available'))
            except Exception as e:
                self.image_label.config(image="", text=get_text('image_error').format(e=e))

    def confirm(self):
        """Confirms the selection and calls the callback."""
        self.player_name = self.name_entry.get()
        if not self.player_name:
            simpledialog.messagebox.showwarning(get_text('missing_name_title'), get_text('missing_name_message'), parent=self)
            return

        if self.callbacks['confirm']:
            self.callbacks['confirm'](self.player_name, self.selected_class_key)
