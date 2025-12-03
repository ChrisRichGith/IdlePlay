# utils.py
"""
Contains utility functions for the game, such as currency formatting.
"""
import tkinter as tk
from PIL import Image, ImageTk
import os

def format_currency(copper_amount):
    """
    Converts a total copper amount into a formatted string (gold, silver, copper).
    100 copper = 1 silver
    100 silver = 1 gold
    """
    if copper_amount == 0:
        return "0c"

    gold = copper_amount // 10000
    silver = (copper_amount % 10000) // 100
    copper = copper_amount % 100

    parts = []
    if gold > 0:
        parts.append(f"{gold}🪙")
    if silver > 0:
        parts.append(f"{silver}💿")
    if copper > 0:
        parts.append(f"{copper}🟤")

    return " ".join(parts)

def center_window(window, parent):
    """
    Centers a tkinter window over its parent window, handling multi-monitor setups.

    Args:
        window: The tkinter window (Toplevel) to center.
        parent: The parent window.
    """
    window.update_idletasks()

    # Get dimensions of the popup window
    width = window.winfo_width()
    height = window.winfo_height()

    # Get the position and dimensions of the parent window
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    # Calculate the center position relative to the parent
    x = parent_x + (parent_width // 2) - (width // 2)
    y = parent_y + (parent_height // 2) - (height // 2)

    # Set the geometry of the popup window to place it correctly
    window.geometry(f'{width}x{height}+{x}+{y}')

def apply_tiled_background(widget, image_path):
    """
    Applies a tiled background image to a widget.
    The image is drawn on a canvas that resizes with the widget.
    """
    # Create a canvas within the widget, placed to fill the entire widget
    canvas = tk.Canvas(widget)
    canvas.place(relwidth=1, relheight=1)

    # Ensure the canvas is at the bottom of the stacking order
    canvas.lower()

    try:
        # Open the image and create a PhotoImage object
        # Store it on the canvas to prevent garbage collection
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        image = Image.open(image_path)
        canvas.image = ImageTk.PhotoImage(image)

        def tile_background(event):
            """Callback to redraw the background when the canvas is resized."""
            # Get canvas dimensions
            canvas_width = event.width
            canvas_height = event.height

            # Clear any previous drawings
            canvas.delete("all")

            # Get image dimensions
            image_width = canvas.image.width()
            image_height = canvas.image.height()

            # Tile the image across the canvas
            for y in range(0, canvas_height, image_height):
                for x in range(0, canvas_width, image_width):
                    canvas.create_image(x, y, anchor="nw", image=canvas.image)

        # Bind the tiling function to the canvas's <Configure> event
        canvas.bind("<Configure>", tile_background)

    except (FileNotFoundError, tk.TclError) as e:
        # Fallback to a solid color if the image fails to load
        print(f"Error loading background image: {e}. Using fallback color.")
        canvas.config(bg="#3B3B3B") # A dark gray as a fallback
